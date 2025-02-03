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
        time.sleep(DELAY_TIME*2)
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
            for x in range(600):
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
        logger('148')

        intro_video_page.enter_intro_video_room()
        time.sleep(DELAY_TIME*10)

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

    def scroll_down_load_template(self, value):
        try:
            drag_result = intro_video_page.drag_scroll_bar_for_template(value)

            scroll_value = -1
            if not drag_result:
                logger('Current scroll bar loading lots template')
                scroll_value = main_page.exist(L.intro_video_room.scroll_bar).AXValue

        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger('---------- line 228 -----------')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            logger('---------- line 231 -----------')
            raise Exception
        return scroll_value

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1(self):
        try:
            high_mem_usage = 0
            intro_video_page.enter_intro_video_room()
            time.sleep(DELAY_TIME * 10)

            # Part 1: Enter Cyberlink category
            self.scroll_down_load_template(0.2)
            self.scroll_down_load_template(0.4)
            self.scroll_down_load_template(0.6)
            self.scroll_down_load_template(0.8)
            self.scroll_down_load_template(1)
            current_usage = cpu_memory_usage.ram
            if current_usage > high_mem_usage:
                high_mem_usage = current_usage
            logger(f'Scan Cyberlink complete: {cpu_memory_usage.ram}')

            # Part 2: Enter Theme -----------

            theme_option = ['Beauty', 'Business', 'Design', 'Education', 'Event', 'Family', 'Fashion', 'Food',
                         'Gaming', 'Health', 'Holiday', 'Life', 'Love', 'Music', 'Nature', 'Pets', 'Repair', 'Retro',
                         'Season', 'Social Media', 'Sport', 'Technology', 'Travel']
            x = 0
            for x in range(23):
                current_category = theme_option[x]
                logger(f'current_category is {current_category}')

                intro_video_page.click_Theme_specific_category(current_category)
                time.sleep(DELAY_TIME * 5)

                # Scroll down loop
                y = 0
                times = 0
                for times in range(100):
                    new_y = y + 0.2
                    #logger(f' current y:{y}, new_y: {new_y}')
                    if new_y >= 1:
                        new_y = 1
                    check_value = self.scroll_down_load_template(new_y)

                    # Next round y value
                    if check_value == -1:
                        y = round(new_y, 2)
                    else:
                        y = round(check_value, 2)
                    #logger(f'next round y = {y}')

                    if y == 1:
                        logger(f'for loop times: {times}')
                        #logger(' y = 1 now')
                        break

                current_usage = cpu_memory_usage.ram
                if current_usage > high_mem_usage:
                    high_mem_usage = current_usage
                logger(f'------- Scan {current_category} complete: {cpu_memory_usage.ram} -----------------------')

            # Scroll (category side) to top when complete Part 2
            main_page.exist(L.intro_video_room.category_scroll_bar).AXValue = 0
            time.sleep(DELAY_TIME * 2)

            # Part 3: Enter Style -----------
            style_option = ['Black & White', 'Fun & Playful', 'Handwritten', 'Minimalist', 'Modern']
            x = 0
            for x in range(5):
                current_category = style_option[x]
                logger(f'current_category is {current_category}')

                intro_video_page.click_Style_specific_category(current_category)
                time.sleep(DELAY_TIME * 5)

                # Scroll down loop
                y = 0
                times = 0
                for times in range(100):
                    new_y = y + 0.2
                    #logger(f' current y:{y}, new_y: {new_y}')
                    if new_y >= 1:
                        new_y = 1
                    check_value = self.scroll_down_load_template(new_y)

                    # Next round y value
                    if check_value == -1:
                        y = round(new_y, 2)
                    else:
                        y = round(check_value, 2)
                    #logger(f'next round y = {y}')

                    if y == 1:
                        logger(f'for loop times: {times}')
                        #logger(' y = 1 now')
                        break

                current_usage = cpu_memory_usage.ram
                if current_usage > high_mem_usage:
                    high_mem_usage = current_usage
                logger(f'------- Scan {current_category} complete: {cpu_memory_usage.ram} -----------------------')

            logger(f'high_mem_usage : {high_mem_usage}')
        except Exception as e:
            logger(f'Exception occurs. log={e}')
            logger(cpu_memory_usage.ram)
            logger(cpu_memory_usage.cpu)
            raise Exception