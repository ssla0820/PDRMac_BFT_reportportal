import sys, os
import tempfile
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
media_room_page = PageFactory().get_page_object('media_room_page', mac)
precut_page = PageFactory().get_page_object('precut_page', mac)
intro_video_page = PageFactory().get_page_object('intro_video_room_page', mac)
download_from_ss_page = PageFactory().get_page_object('download_from_shutterstock_page', mac)
getty_image_page = PageFactory().get_page_object('gettyimage_page', mac)
title_designer_page = PageFactory().get_page_object('title_designer_page', mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="Pre Cut.html")
cpu_memory_usage = report.get_driver(0)
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
#Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/GroundTruth/Pre_Cut/'
#Auto_Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/ATGroundTruth/Pre_Cut/'
#Test_Material_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/'
Ground_Truth_Folder = app.ground_truth_root + '/Intro_Video_Room/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Intro_Video_Room/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Scan_Intro_Video():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        # Get "mac_driver" path
        temp_dir = os.path.abspath(tempfile.gettempdir() + "/mac_driver")
        logger(temp_dir)

        # delete mac_driver
        main_page.delete_folder(temp_dir)

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
            google_sheet_execution_log_init('Test_Scan_Intro_Video')

    @classmethod
    def teardown_class(cls):
        logger('Test Case are completed.')
        '''
        logger('teardown_class - export report')
        report.export()
        logger(
            f"Pre Cut result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()
        '''

    def find_Video_Intro_sub_category_count(self):
        try:
            time.sleep(DELAY_TIME * 10)

            # Find index
            round = 0
            for x in range(800):
                logger(x)
                img_before = main_page.snapshot(locator=L.base.Area.preview.main)
                time.sleep(DELAY_TIME*0.5)
                main_page.keyboard.press(main_page.keyboard.key.down)
                time.sleep(DELAY_TIME * 2)
                img_after = main_page.snapshot(locator=L.base.Area.preview.main)
                check_no_change = main_page.compare(img_before, img_after, similarity=0.98)
                logger(check_no_change)

                # library preview does not change, leave for loop
                if check_no_change == True:
                    break
                else:
                    round = round + 1

            logger(round)
            #child_list = self.exist(L.intro_video_room.library_collection_view).AXChildren
            #count = len(child_list)
            count = round * 5
            logger(count)
            time.sleep(DELAY_TIME*2)
            scroll_bar = main_page.exist(L.intro_video_room.scroll_bar)
            if scroll_bar:
                intro_video_page.drag_scroll_bar_for_template(0)

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return count

    def check_Library_Preview(self, mid_duration):
        time.sleep(5)
        value = int(mid_duration)
        # timecode = 0s
        img_before = intro_video_page.snapshot(locator=L.base.Area.preview.main)

        # Click [Play] then pause
        main_page.press_space_key()

        # if mid_duration is too short, enlarge the delay time
        if value < 4:
            time.sleep(DELAY_TIME*2)

        time.sleep(DELAY_TIME * value)
        main_page.press_space_key()
        img_after = intro_video_page.snapshot(locator=L.base.Area.preview.main)
        library_preview_result = main_page.compare(img_before, img_after, similarity=1)
        return library_preview_result

    def check_Designer_Preview(self, mid_duration):
        value = int(mid_duration)
        # Set timecode to 1s, then snapshot
        intro_video_page.set_designer_timecode('01_00')
        time.sleep(DELAY_TIME)
        img_before = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)

        # Set timecode to mid_duration * 2 - 1, then snapshot
        final_value = value*2-1
        logger(final_value)
        if final_value < 10:
            intro_video_page.set_designer_timecode(f'0_{final_value}_00')
        else:
            intro_video_page.set_designer_timecode(f'{final_value}_00')
        time.sleep(DELAY_TIME)
        img_after = intro_video_page.snapshot(locator=L.intro_video_room.intro_video_designer.preview_area)
        designer_preview_result = main_page.compare(img_before, img_after, similarity=1)
        return designer_preview_result

    def check_Timeline_Preview(self, mid_duration):
        value = int(mid_duration)
        # Set timecode to 2s, then snapshot
        main_page.set_timeline_timecode('00_00_02_00')
        time.sleep(DELAY_TIME)
        img_before = intro_video_page.snapshot(locator=L.base.Area.preview.main)

        # Set timecode to mid_duration + 1, then snapshot
        final_value = value+1
        logger(final_value)
        if final_value < 10:
            main_page.set_timeline_timecode(f'00_00_0{final_value}_00')
        else:
            main_page.set_timeline_timecode(f'00_00_{final_value}_00')
        time.sleep(DELAY_TIME)
        img_after = intro_video_page.snapshot(locator=L.base.Area.preview.main)
        timeline_preview_result = main_page.compare(img_before, img_after, similarity=1)
        return timeline_preview_result

    def close_PDR_then_enter_Intro_room(self):
        main_page.close_app()
        time.sleep(DELAY_TIME * 2)
        main_page.clear_cache()
        time.sleep(DELAY_TIME)

        main_page.start_app()
        time.sleep(DELAY_TIME*15)

        # If pop up Seasonal BB
        if main_page.exist(L.base.seasonal_bb_window.main):
            # Close seasonal BB dialog
            main_page.press_esc_key()
            time.sleep(1)

        # Enter Intro Room
        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME*10)

    def check_open_intro_template(self):
        check_open_status = False
        # Downloading template for open Intro designer
        for x in range(15):
            check_open_status = intro_video_page.check_in_intro_designer()
            if check_open_status:
                break
            else:
                time.sleep(DELAY_TIME)

        # Loading template when open intro template
        check_loading_status = False
        for x in range(15):
            check_loading_status = main_page.is_not_exist(L.download_from_shutterstock.download.frame)
            if check_loading_status:
                logger('loading complete')
                break
            else:
                time.sleep(DELAY_TIME*3)
        return check_loading_status

    def sort_by_date(self):
        try:
            if not main_page.exist_click(L.media_room.library_menu.btn_menu):
                raise Exception

            if not main_page.select_right_click_menu('Sort by', 'Date'):
                raise Exception

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    def from_view_template_to_enter_intro_outro_designer(self):
        try:
            # Click [Edit in Intro Video Designer]
            main_page.click(L.intro_video_room.view_template_dialog.btn_edit_in_Intro_Desinger)
            time.sleep(DELAY_TIME * 3)
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            raise Exception
        return True

    @pytest.mark.skip
    @exception_screenshot
    def test_1_1(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Outro
            current_category = 'Outro'
            intro_video_page.enter_season_theme_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 70
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_1/2_1_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.enter_season_theme_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_2(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Valentine\'s Day
            # Get sub category : Mother\'s Day
            current_category = 'Birthday'
            time.sleep(DELAY_TIME * 3)
            intro_video_page.enter_season_theme_category(current_category)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 70
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/1_2/1_2_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 4)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.enter_season_theme_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_3(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Birthday
            current_category = 'Countdown'
            time.sleep(DELAY_TIME * 3)
            intro_video_page.enter_season_theme_category(current_category)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/1_3/1_3_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.enter_season_theme_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_4(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Spring
            current_category = 'Wedding'
            time.sleep(DELAY_TIME * 3)
            intro_video_page.enter_season_theme_category(current_category)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 60
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/1_4/1_4_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()
                time.sleep(DELAY_TIME * 2)
                # Check open intro template
                self.check_open_intro_template()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.enter_season_theme_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Beauty
            current_category = 'Beauty'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_1/2_1_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_2(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Business
            current_category = 'Business'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_2/2_2_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_3(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Design
            current_category = 'Design'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_3/2_3_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_4(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Education
            current_category = 'Education'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_4/2_4_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_5(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Event
            current_category = 'Event'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 70
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_5/2_5_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_6(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Family
            current_category = 'Family'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_6/2_6_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_7(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Fashion
            current_category = 'Fashion'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_7/2_7_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()
                # Check open intro template
                self.check_open_intro_template()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_8(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Food
            current_category = 'Food'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_8/2_8_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_9(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Gaming
            current_category = 'Gaming'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_9/2_9_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception


    # @pytest.mark.skip
    @exception_screenshot
    def test_2_10(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Health
            current_category = 'Health'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_10/2_10_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_11(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Holiday
            current_category = 'Holiday'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_11/2_11_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_12(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Life
            current_category = 'Life'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 70
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_12/2_12_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_13(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Love
            current_category = 'Love'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_13/2_13_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_14(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Music
            current_category = 'Music'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_14/2_14_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_15(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Nature
            current_category = 'Nature'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 70
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_15/2_15_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_16(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Pets
            current_category = 'Pets'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_16/2_16_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_17(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Repair
            current_category = 'Repair'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_17/2_17_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_18(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Retro
            current_category = 'Retro'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_18/2_18_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_19(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Season
            current_category = 'Season'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 60
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_19/2_19_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_20(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Social Media
            current_category = 'Social Media'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 60
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_20/2_20_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_21(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Sport
            current_category = 'Sport'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_21/2_21_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_22(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Technology
            current_category = 'Technology'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_22/2_22_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_23(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Travel
            current_category = 'Travel'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 70
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/2_23/2_23_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_1(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME*5)
            # Get sub category : Black & White
            current_category = 'Black & White'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')
    
            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')
    
            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)
    
                intro_video_page.select_intro_template_method_2(index)
    
                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME*10)
    
                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                 file_name=Ground_Truth_Folder + f'/3_1/3_1_{index}.png')
                logger(current_image)
    
                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()
    
                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME*2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)
    
                main_page.press_esc_key()
    
                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()
    
                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)
    
                # Step4:
                # Check Designer Preview
    
                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME*5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)
    
                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()
    
                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME*3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)
    
                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')
    
                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME*2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME*2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)
    
                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
    
                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_2(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Fun & Playful
            current_category = 'Fun & Playful'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 70
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/3_2/3_2_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_3(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Handwritten
            current_category = 'Handwritten'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 40
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/3_3/3_3_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_4(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Minimalist
            current_category = 'Minimalist'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 70
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/3_4/3_4_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_5(self):
        try:
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 5)
            # Get sub category : Modern
            current_category = 'Modern'
            intro_video_page.click_intro_specific_category(current_category)
            time.sleep(DELAY_TIME * 3)

            # Sort by date
            self.sort_by_date()
            time.sleep(DELAY_TIME * 5)
            get_count = self.find_Video_Intro_sub_category_count()
            logger(f' {current_category} has {get_count} template')

            index = 1
            loop_times = 70
            # get_count < 60, loop time use get_count value
            if get_count < loop_times:
                loop_times = get_count
            logger(f'Now loop_time: {loop_times}')

            for x in range(loop_times):
                logger(f'Selected {index} template:')
                time.sleep(DELAY_TIME)

                intro_video_page.select_intro_template_method_2(index)

                # Step1:
                # Open View Template to snapshot one image then save image in ground truth folder
                intro_video_page.open_view_template()
                time.sleep(DELAY_TIME * 10)

                current_image = intro_video_page.snapshot(locator=L.intro_video_room.view_template_dialog.main_window,
                                                          file_name=Ground_Truth_Folder + f'/3_5/3_5_{index}.png')
                logger(current_image)

                # Click [Edit in Intro Video Designer]
                self.from_view_template_to_enter_intro_outro_designer()

                # Step2:
                # Get template its total duration > Then close designer
                for extra_x in range(50):
                    current_mid = intro_video_page.get_designer_timecode_only_sec()
                    if current_mid:
                        time.sleep(DELAY_TIME * 2)
                        break
                    time.sleep(DELAY_TIME)
                logger(f' this template\'s mid duration is {current_mid} sec')
                time.sleep(DELAY_TIME)

                main_page.press_esc_key()

                # Verify close designer
                # if not close ready, press esc again
                if main_page.is_exist(L.intro_video_room.intro_video_designer.main_window):
                    logger('801')
                    main_page.press_esc_key()

                # Step3:
                # Check Library Preview
                library_result = not self.check_Library_Preview(current_mid)
                logger(library_result)

                # Step4:
                # Check Designer Preview

                intro_video_page.select_then_enter_designer(index)
                time.sleep(DELAY_TIME * 5)
                designer_result = not self.check_Designer_Preview(current_mid)
                logger(designer_result)

                # Step5:
                # In Designer, Click [Add to Timeline]
                intro_video_page.click_btn_add_to_timeline()

                # Step6:
                # Check Timeline Preview
                time.sleep(DELAY_TIME * 3)
                timeline_result = not self.check_Timeline_Preview(current_mid)
                logger(timeline_result)

                # Step7:
                # library_result and designer_result and timeline_result = True
                # remove the snapshot
                scan_result = library_result and designer_result and timeline_result
                logger(f'Template {index} result is {scan_result}')
                if scan_result:
                    main_page.delete_folder(current_image)
                    logger('remove done')

                # Tap New Workspace hotkey
                time.sleep(DELAY_TIME * 2)
                main_page.tap_NewWorkspace_hotkey()
                time.sleep(DELAY_TIME * 2)
                main_page.handle_no_save_project_dialog()
                time.sleep(DELAY_TIME * 2)

                # Step8:
                # (Scroll bar to drag down)
                # If index = 30th, 60th, 90th,... >> close_PDR_then_enter_Intro_room()
                time.sleep(DELAY_TIME * 0.5)
                if (index == 15):
                    intro_video_page.scroll_down_to_template_visual_area(index)
                    time.sleep(DELAY_TIME * 0.5)
                elif (index > 15) & (index % 10 == 0):
                    # scroll down for 21th, 31h, 41th, ...
                    # scroll timing is 20th scan complete
                    x1_th = index + 1
                    if (index % 30 == 0):
                        # Close AP then re-launch
                        self.close_PDR_then_enter_Intro_room()
                        intro_video_page.click_intro_specific_category(current_category)
                        time.sleep(DELAY_TIME * 5)
                        # Sort by date
                        self.sort_by_date()
                        time.sleep(DELAY_TIME * 5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)
                    else:
                        intro_video_page.drag_scroll_bar_for_template(0)
                        time.sleep(DELAY_TIME * 0.5)
                        intro_video_page.scroll_down_to_template_visual_area(x1_th)
                        time.sleep(DELAY_TIME * 0.5)

                # Step9:  Index + 1
                index = index + 1

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception

    @pytest.mark.skip
    @exception_screenshot
    def test_page_function_check(self):
        #intro_video_page.click_btn_save_as('III')
        #intro_video_page.enter_saved_category()

        #intro_video_page.click_btn_close()
        #result = intro_video_page.get_designer_title()
        #result = intro_video_page.click_menu_bar_help()
        #logger(result)
        #intro_video_page.click_undo_button()
        #intro_video_page.click_redo_button()
        #intro_video_page.click_max_restore_btn()
        #intro_video_page.click_max_restore_btn()
        #intro_video_page.click_upper_close_btn()
        #intro_video_page.handle_warning_save_change_before_leaving('Cancel')
        #intro_video_page.handle_warning_save_change_before_leaving('No')
        #result = intro_video_page.click_DZ_btn()
        #logger(result)
        #intro_video_page.click_preview_operation('Play')
        #time.sleep(DELAY_TIME)
        #intro_video_page.click_preview_operation('Pause')
        #time.sleep(DELAY_TIME)
        #intro_video_page.click_preview_operation('Play')
        #time.sleep(DELAY_TIME)
        #intro_video_page.click_preview_operation('Stop')
        #intro_video_page.click_preview_center()
        #intro_video_page.click_preview_left_upper()
        #intro_video_page.click_replace_media(1)
        #main_page.select_file(Test_Material_Folder+'1.jpg')
        '''
        intro_video_page.click_replace_media(3)
        time.sleep(5)
        getty_image_page.switch_to_GI()
        time.sleep(3)
        download_from_ss_page.click_next_page()
        time.sleep(3)
        download_from_ss_page.video.select_thumbnail_for_video_intro_designer(1)
        media_room_page.handle_high_definition_dialog(option='no')

        intro_video_page.click_crop_btn()
        time.sleep(2)
        intro_video_page.crop_zoom_pan.resize_to_small()
        intro_video_page.crop_zoom_pan.leave_crop('Yes')

        intro_video_page.click_add_text(2)
        time.sleep(1)
        #intro_video_page.cancel_selection_button()


        intro_video_page.click_add_text(1)
        time.sleep(1)
        intro_video_page.general_title.click_backdrop_button()
        time.sleep(1)
        intro_video_page.cancel_selection_button()

        intro_video_page.general_title.click_animation_button()
        time.sleep(1)
        intro_video_page.cancel_selection_button()

        intro_video_page.general_title.click_remove_button()
        time.sleep(1)
        #intro_video_page.cancel_selection_button()

        intro_video_page.backdrop_settings.enable_backdrop(1)
        result = intro_video_page.backdrop_settings.get_backdrop_checkbox()
        logger(result)

        intro_video_page.backdrop_settings.set_type(2, fit_type=4)
        result = intro_video_page.backdrop_settings.get_type()
        logger(result)
        result = intro_video_page.backdrop_settings.get_fit_backdrop_status()
        logger(result)


        intro_video_page.backdrop_settings.set_uniform_color('1E8341')
        result = intro_video_page.backdrop_settings.get_uniform_color()
        logger(result)

        # result = intro_video_page.backdrop_settings.click_close_btn()
        #logger(result)

        #result = download_from_ss_page.close_pop_up_preview_window()
        #logger(result)

        #title_designer_page.handle_effect_want_to_continue()
        intro_video_page.general_title.in_animation.select_specific_effect_combobox(6)
        check_result = intro_video_page.general_title.in_animation.get_effect_dropdownmenu()
        logger(check_result)


        #intro_video_page.general_title.in_animation.unfold_setting(0)
        #result = intro_video_page.general_title.in_animation.get_unfold_setting()
        #logger(result)
        intro_video_page.general_title.in_animation.unfold_setting(1)
        result = intro_video_page.general_title.in_animation.get_unfold_setting()
        logger(result)
        intro_video_page.general_title.in_animation.select_template(2)


        intro_video_page.general_title.out_animation.select_specific_effect_combobox(3)
        check_result = intro_video_page.general_title.out_animation.get_effect_dropdownmenu()
        logger(check_result)


        intro_video_page.general_title.out_animation.unfold_setting(0)
        intro_video_page.general_title.out_animation.unfold_setting(1)
        result = intro_video_page.general_title.out_animation.get_unfold_setting()
        logger(result)

        intro_video_page.general_title.out_animation.select_template(5)
        time.sleep(DELAY_TIME*2)
        intro_video_page.general_title.close_animation_window()

        intro_video_page.motion_graphics.select_template(index=3, category=3)

        result = intro_video_page.motion_graphics.click_settings_button()
        logger(result)
        result = intro_video_page.motion_graphics.click_remove_button()
        logger(result)

        intro_video_page.motion_graphics.set_title_text('12WRg ETGBG')
        result = intro_video_page.motion_graphics.get_title_text()
        logger(result)

        intro_video_page.motion_graphics.set_font_color('B927A1')
        result = intro_video_page.motion_graphics.get_font_color()
        logger(result)

        intro_video_page.motion_graphics.click_close_btn()

        intro_video_page.click_duration_btn()
        #intro_video_page.duration_setting.click_OK()
        #result = intro_video_page.duration_setting.get_org_duration()
        #logger(result)
        intro_video_page.duration_setting.set_new_duration(value=6)
        result = intro_video_page.duration_setting.get_new_duration()
        logger(result)

        intro_video_page.motion_graphics.select_title_category('Add Title Here')

        intro_video_page.click_add_image(2)
        intro_video_page.image.click_object_settings_btn()
        intro_video_page.image.click_animation_btn()
        intro_video_page.image.click_replace_btn()
        intro_video_page.image.click_remove_button()
        intro_video_page.image.object_settings.unfold_border(0)
        result = intro_video_page.image.object_settings.get_border_unfold_setting()
        logger(result)
        intro_video_page.image.object_settings.enable_border(1)
        result = intro_video_page.image.object_settings.get_border_status()
        logger(result)

        intro_video_page.image.object_settings.set_border_size(3)
        result = intro_video_page.image.object_settings.get_border_size()
        logger(result)
        intro_video_page.image.object_settings.set_border_size(6)
        result = intro_video_page.image.object_settings.get_border_size()
        logger(result)
        intro_video_page.image.object_settings.click_close_btn()
        intro_video_page.image.in_animation.unfold_setting(1)
        intro_video_page.image.in_animation.unfold_setting(0)

        intro_video_page.image.out_animation.unfold_setting(1)
        intro_video_page.image.out_animation.unfold_setting(0)
        intro_video_page.image.in_animation.select_template('Brush Transition 03')
        intro_video_page.image.out_animation.select_template('Basic Shape 04')
        intro_video_page.image.close_animation_window()
        '''
        intro_video_page.click_add_pip_object()
        intro_video_page.select_pip_template(3)
        intro_video_page.cancel_selection_button()
        intro_video_page.click_add_pip_object()
        intro_video_page.select_pip_template(5, 'Social Media')