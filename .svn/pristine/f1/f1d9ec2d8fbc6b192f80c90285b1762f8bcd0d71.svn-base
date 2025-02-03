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
import_media_from_cloud_page = PageFactory().get_page_object('import_downloaded_media_from_cl_page', mwc)
download_from_cl_dz_page = PageFactory().get_page_object('download_from_cl_dz_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
download_from_shutterstock_page = PageFactory().get_page_object('download_from_shutterstock_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Media Import-Download Media from CyberLink Cloud.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Import_Media_from_Cloud/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Import_Media_from_Cloud/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1


class Test_Import_Media_From_Cloud():
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
            google_sheet_execution_log_init('Import_Media_from_Cloud')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"import media from cloud result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        with uuid('970882f2-aca3-4893-b227-4fc387e42541') as case:
            # 1. General
            # 1.1. Entrance
            # 1.1.2. Right click on space place > [ Download From ] > [ Download Media from CyberLink Cloud… ]
            # Pop up the Download Media window.
            media_room_page.collection_view_deselected_media()
            media_room_page.right_click()
            media_room_page.select_right_click_menu('Download from', 'Download Media from CyberLink Cloud...')
            is_in_download_media = import_media_from_cloud_page.is_exist(
                L.import_downloaded_media_from_cl.downloaded_media_window, timeout=10)
            case.result = False if not is_in_download_media else True

            for check_template_ready in range(10):  # waiting for media content list ready
                template_ready = import_media_from_cloud_page.find(
                    L.import_downloaded_media_from_cl.select_deselect_all_btn, timeout=10).AXEnabled
                if not template_ready:
                    time.sleep(DELAY_TIME)
                    continue
                else:
                    break

        with uuid('cc1b837d-d1e6-42da-9da6-5914a1835aae') as case:
            # 1.2. Caption Bar
            # 1.2.1. General Functions > [Refresh] > Folder
            # update folders created from web page
            check_result_1 = import_media_from_cloud_page.tap_refresh_btn()
            time.sleep(DELAY_TIME * 2)
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_1_2_1-1.png', 'Download Media Window')
            case.result = check_result_1 and check_result_2

        with uuid('76c5676c-14d8-4056-a0b3-4d2b7306a64c') as case:
            # 1.2. Caption Bar
            # 1.2.1. General Functions > [Refresh] > File
            # Update files uploaded from other platforms or web page.
            import_media_from_cloud_page.double_click_folder(folder_index=1)
            time.sleep(DELAY_TIME)
            check_result_1 = import_media_from_cloud_page.tap_refresh_btn()
            time.sleep(DELAY_TIME*2)
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_1_2_1-2.png', 'Download Media Window')
            case.result = check_result_1 and check_result_2

            time.sleep(DELAY_TIME * 3)

        with uuid('26e10073-df24-4ec7-9e15-f1def07c1ece') as case:
            # 1.2. Caption Bar
            # 1.2.1. General Functions > [ X ] > Close
            # Close the Download Media window.
            download_from_cl_dz_page.tap_close_button()

            is_in_download_media = import_media_from_cloud_page.is_not_exist(
                L.import_downloaded_media_from_cl.downloaded_media_window, timeout=10)
            check_result = False if not is_in_download_media else True
            case.result = check_result

        with uuid('27fdf436-a466-43d0-8515-d2ba41f13e4c') as case:
            # 1.1. Entrance
            # 1.1.3. Caption bar > [ File ] > [ Import ] > [ Download Media from CyberLink Cloud… ]
            # Pop up the Download Media window
            time.sleep(3)
            main_page.top_menu_bar_file_import_download_media_from_cl_cloud()

            is_in_download_media = import_media_from_cloud_page.is_exist(
                L.import_downloaded_media_from_cl.downloaded_media_window, timeout=10)
            check_result = False if not is_in_download_media else True
            case.result = check_result

        with uuid('814d60f9-9088-44f1-982a-00f10f023919') as case:
            # 1.2. Caption Bar
            # 1.2.2. Caption Name > Download Media
            # display "Download Media" on the caption bar
            caption_name = main_page.exist([L.import_downloaded_media_from_cl.downloaded_media_window, [{'AXRole' : 'AXToolbar'}, {"AXRole": "AXStaticText"}]]).AXValue
            case.result = False if not caption_name == 'Download Media' else True

        with uuid('0602be6c-19e9-43db-8e02-68de0c85ce21') as case:
            # 1.2. Caption Bar
            # 1.2.1. General Functions > [esc] > Hotkey
            # Close the Download Media window
            import_media_from_cloud_page.press_esc_key()
            is_in_download_media = import_media_from_cloud_page.is_not_exist(
                L.import_downloaded_media_from_cl.downloaded_media_window, timeout=10)
            check_result = False if not is_in_download_media else True
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        media_room_page.import_media_from_cyberlink_cloud()
        import_media_from_cloud_page.is_exist(L.import_downloaded_media_from_cl.downloaded_media_window, timeout=10)
        for check_template_ready in range(10):
            template_ready = import_media_from_cloud_page.find(
                L.import_downloaded_media_from_cl.select_deselect_all_btn, timeout=10).AXEnabled
            if not template_ready:
                time.sleep(DELAY_TIME)
                continue
            else:
                break

        import_media_from_cloud_page.switch_to_video_page()

        with uuid('fa53657e-e946-4dee-925f-4be5a799bfb5') as case:
            # 2. Video
            # 2.1. General Function
            # 2.1.1. Selection > [Select all/Deselect all] > Folder
            # all folders are selected/deselected
            check_result_1 = import_media_from_cloud_page.tap_select_deselect_all_btn()  # select all
            time.sleep(DELAY_TIME)
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_1_1-1.png', 'Download Media Window')

            check_result_3 = import_media_from_cloud_page.tap_select_deselect_all_btn()  # deselect all
            time.sleep(DELAY_TIME)
            check_result_4 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_1_1-2.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('29b00f72-67c1-40e6-af5a-59706df353db') as case:
            # 2.1. General Function
            # 2.1.1. Selection > Single select > Folder
            # can select/deselect single folder by ticking the checkbox
            check_result_1 = import_media_from_cloud_page.select_content_in_folder_level(
                folder_index=0, click_times=1)  # check
            time.sleep(DELAY_TIME)
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_1_1-3.png', 'Download Media Window')

            check_result_3 = import_media_from_cloud_page.select_content_in_folder_level(
                folder_index=0, click_times=1)  # uncheck
            check_result_4 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_1_1-4.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('5f73d3e7-ed4f-4444-b632-44d1836a88e7') as case:
            # 2.1. General Function
            # 2.1.1. Selection > Multiple select > Folder
            # can select/deselect multiple folders by ticking the checkbox
            import_media_from_cloud_page.select_content_in_folder_level(folder_index=0, click_times=1)  # check
            import_media_from_cloud_page.select_content_in_folder_level(folder_index=1, click_times=1)  # check
            time.sleep(DELAY_TIME)
            check_result_1 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_1_1-5.png', 'Download Media Window')

            import_media_from_cloud_page.select_content_in_folder_level(folder_index=0, click_times=1)  # uncheck
            import_media_from_cloud_page.select_content_in_folder_level(folder_index=1, click_times=1)  # uncheck
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_1_1-6.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('ccbb1473-9fdb-4276-9e5f-8af7ea7624c4') as case:
            # 2.1. General Function
            # 2.1.2. Folder <-> File > Double-click the folder
            # enter the folder to file level
            check_result_1 = import_media_from_cloud_page.select_content_in_folder_level(
                folder_index=0, click_times=2)  # into a folder
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_1_2-1.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('13fc7e40-081e-43b9-8169-83b98c8b43d2') as case:
            # 2.1. General Function
            # 2.1.1. Selection > [Select all/Deselect all] > File
            # all files are selected/deselected
            check_result_1 = import_media_from_cloud_page.tap_select_deselect_all_btn()  # select all
            time.sleep(DELAY_TIME)
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_1_1-7.png', 'Download Media Window')

            check_result_3 = import_media_from_cloud_page.tap_select_deselect_all_btn()  # deselect all
            check_result_4 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_1_1-8.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('5a02acc9-aba4-4593-a976-5beb6181d9c5') as case:
            # 2.1. General Function
            # 2.1.1. Selection > Single select > File
            # can select/deselect single file by ticking the checkbox
            check_result_1 = import_media_from_cloud_page.select_content_in_file_level(file_index=1)  # check
            time.sleep(DELAY_TIME)
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_1_1-9.png', 'Download Media Window')

            check_result_3 = import_media_from_cloud_page.select_content_in_file_level(file_index=1)  # uncheck
            check_result_4 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_1_1-10.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('1bf4afa5-6bf2-46fe-a823-a0f75b9ed088') as case:
            # 2.1. General Function
            # 2.1.1. Selection > Multiple select > File
            # can select/deselect multiple files by ticking the checkbox
            import_media_from_cloud_page.select_content_in_file_level(file_index=1)  # check
            import_media_from_cloud_page.select_content_in_file_level(file_index=2)  # check
            time.sleep(DELAY_TIME)
            check_result_1 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_1_1-11.png', 'Download Media Window')

            import_media_from_cloud_page.select_content_in_file_level(file_index=1)  # uncheck
            import_media_from_cloud_page.select_content_in_file_level(file_index=2)  # uncheck
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_1_1-12.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('d18304d9-deef-4d8c-a316-ee82e5bf64a9') as case:
            # 2.1. General Function
            # 2.1.1. Selection > # clip(s) selected > Number
            # the number should match the quantity of selected clips
            import_media_from_cloud_page.tap_select_deselect_all_btn()  # select all
            time.sleep(DELAY_TIME)
            count_clips_selected = import_media_from_cloud_page.find(
                L.import_downloaded_media_from_cl.txt_clips_selected).AXValue

            case.result = False if not count_clips_selected == '4 clip(s) selected' else True

        with uuid('72af5c2d-d2c1-4066-9bd2-fc85d23e7dc6') as case:
            # 2.1. General Function
            # 2.1.2. Folder <-> File > [Up One Level]
            # back to the previous level
            check_result_1 = import_media_from_cloud_page.back_to_previous_level()
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_1_2-2.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        media_room_page.import_media_from_cyberlink_cloud()
        import_media_from_cloud_page.is_exist(L.import_downloaded_media_from_cl.downloaded_media_window, timeout=10)
        for check_template_ready in range(10):
            template_ready = import_media_from_cloud_page.find(
                L.import_downloaded_media_from_cl.select_deselect_all_btn, timeout=10).AXEnabled
            if not template_ready:
                time.sleep(DELAY_TIME)
                continue
            else:
                break

        import_media_from_cloud_page.switch_to_video_page()

        with uuid('fd21babc-58f2-4888-a09d-6fd4ce63907c') as case:
            # 2.2. Folder Level
            # 2.2.1. Search > Default text
            # show 'search the library' in the search bar
            default_text = import_media_from_cloud_page.exist(
                L.import_downloaded_media_from_cl.search_textfield).AXPlaceholderValue
            case.result = False if not default_text == 'Search the library' else True

        with uuid('20aca1f3-83a5-4b2f-826c-2b88a78faefd') as case:
            # 2.2. Folder Level
            # 2.2.1. Search > Name > Folder Name
            # show folders with entered text
            check_result_1 = import_media_from_cloud_page.input_text_in_seacrh_library('01')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_2_1-1.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

            import_media_from_cloud_page.clear_keyword_in_search_library()

        with uuid('1e84789d-f58c-4448-aaa5-2ef68e175dfb') as case:
            # 2.2. Folder Level
            # 2.2.1. Search > Name > File Name
            # show folders with entered text
            import_media_from_cloud_page.select_content_in_folder_level(folder_index=0, click_times=2)
            check_result_1 = import_media_from_cloud_page.input_text_in_seacrh_library('kid')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_2_1-2.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2
            import_media_from_cloud_page.clear_keyword_in_search_library()

        with uuid('02e34086-90a9-4562-82f9-da563e8cf998') as case:
            # 2.2. Folder Level
            # 2.2.1. Search > No search result
            # show "No clips match the search"
            check_result_1 = import_media_from_cloud_page.input_text_in_seacrh_library('xyz')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_2_1-3.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2
            import_media_from_cloud_page.tap_refresh_btn()

        with uuid('760a97fa-69cd-4e05-bb5a-0154c975f4e3') as case:
            # 2.2. Folder Level
            # 2.2.2. [Library menu] > [Sort By] > Default
            # sort by "Upload Date"
            import_media_from_cloud_page.tap_library_menu_btn()
            import_media_from_cloud_page.tap_sort_by_item()
            default_setting = import_media_from_cloud_page.exist(
                L.import_downloaded_media_from_cl.sort_by_upload_date).AXMenuItemMarkChar
            case.result = False if not default_setting == '✓' else True

            import_media_from_cloud_page.tap_refresh_btn()

        with uuid('fb91b1cd-6605-45b5-82fc-a51e3a17695b') as case:
            # 2.2. Folder Level
            # 2.2.2. [Library menu] > [Sort By] > [Name]
            # can be sorted by name normally
            import_media_from_cloud_page.tap_library_menu_btn()
            import_media_from_cloud_page.tap_sort_by_item()
            check_result_1 = import_media_from_cloud_page.apply_sort_by_type(strType='Name')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_2_2-1.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('0d6851fe-df42-46e2-8915-7334d445cc9f') as case:
            # 2.2. Folder Level
            # 2.2.2. [Library menu] > [Sort By] > [Upload Date]
            # can be sorted by upload date normally
            import_media_from_cloud_page.tap_library_menu_btn()
            import_media_from_cloud_page.tap_sort_by_item()
            check_result_1 = import_media_from_cloud_page.apply_sort_by_type(strType='Upload Date')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_2_2-2.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('dbabbfe0-c75e-4780-bde2-0570cc1aab64') as case:
            # 2.2. Folder Level
            # 2.2.2. [Library menu] > Icons size > Default
            # thumbnails show as medium icons
            import_media_from_cloud_page.tap_library_menu_btn()
            default_setting = import_media_from_cloud_page.exist(
                L.import_downloaded_media_from_cl.medium_icon).AXMenuItemMarkChar
            case.result = False if not default_setting == '✓' else True

            import_media_from_cloud_page.tap_refresh_btn()

        with uuid('798d86c2-5033-461e-98d5-c25da3776641') as case:
            # 2.2. Folder Level
            # 2.2.2. [Library menu] > Icons size > [Extra Large Icons]
            # thumbnails show as extra large icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Extra')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_2_2-3.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('3a8b080c-f5c3-434a-96ca-e1fc96a9ea1c') as case:
            # 2.2. Folder Level
            # 2.2.2. [Library menu] > Icons size > [Large Icons]
            # thumbnails show as large icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Large')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_2_2-4.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('d83bdc40-1cc1-41fc-8f40-5d9efccc45ee') as case:
            # 2.2. Folder Level
            # 2.2.2. [Library menu] > Icons size > [Small Icons]
            # thumbnails show as small icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Small')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_2_2-5.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('30a123ac-b54e-4b2b-9bf3-f1491791b2fb') as case:
            # 2.2. Folder Level
            # 2.2.2. [Library menu] > Icons size > [Medium Icons]
            # thumbnails show as medium icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Medium')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_2_2-6.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('c3b8777e-1a4e-4aca-9cbd-10a2bab77f31') as case:
            # 2.2. Folder Level
            # 2.2.3. Thumbnail > Aspect ratio
            # show the 16:9 ratio in the center of the picture
            import_media_from_cloud_page.highlight_download_media_content(folder_index=0)
            time.sleep(DELAY_TIME * 2)

            check_result = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_2_3-1.png', 'Download Media Window')
            case.result = check_result

            import_media_from_cloud_page.select_content_in_folder_level(folder_index=0, click_times=1)

        with uuid('51150a8f-fc3e-4352-b73a-6049d41ea26d') as case:
            # 2.2. Folder Level
            # 2.2.3. Thumbnail > Checkbox
            # show checkbox normally in upper right corner
            case.result = check_result

        with uuid('0d5cc8a6-6922-4cfc-8789-db5347532537') as case:
            # 2.2. Folder Level
            # 2.2.5. [Download] > No folders selected > Default
            # button is disabled
            button_status = import_media_from_cloud_page.find(L.import_downloaded_media_from_cl.download_btn).AXEnabled
            case.result = True if not button_status else False

        with uuid('bcd79bb4-3f5b-4438-b118-9a83c5c732a8') as case:
            # 2.2. Folder Level
            # 2.2.5. [Download] > select folder(s)
            # button is enabled
            import_media_from_cloud_page.select_content_in_folder_level(folder_index=1, click_times=1)
            time.sleep(3)
            button_status = import_media_from_cloud_page.find(L.import_downloaded_media_from_cl.download_btn).AXEnabled
            case.result = False if not button_status else True

        with uuid('616c6dde-89a4-4f36-9bb6-d90d0b605845') as case:
            # 2.2. Folder Level
            # 2.2.5. [Download] > [Cancel]
            # cancel downloading
            import_media_from_cloud_page.tap_download_btn()
            check_result = import_media_from_cloud_page.tap_cancel_btn()
            case.result = check_result

        with uuid('c096f08f-ae62-4c85-b150-2ec04370dc9e') as case:
            # 2.2. Folder Level
            # 2.2.5. [Download] > complete > Dialog
            # Pop up a dialog "The clips are successfully downloaded and…"
            import_media_from_cloud_page.tap_download_btn()

            for x in range(60):
                result = media_room_page.is_show_high_definition_dialog()
                if result:
                    media_room_page.handle_high_definition_dialog()
                    break
                else:
                    time.sleep(1)

            time.sleep(DELAY_TIME * 2)
            case.result = import_media_from_cloud_page.tap_ok_btn()
            time.sleep(DELAY_TIME * 11)

        with uuid('7e4ebdbe-aff1-405d-be89-4db79bdce60f') as case:
            # 2.2. Folder Level
            # 2.2.5. [Download] > Download downloaded > Dialog
            # Pop up a dialog "The clips were successfully downloaded and…".
            import_media_from_cloud_page.tap_download_btn()
            time.sleep(DELAY_TIME * 3)
            check_result = import_media_from_cloud_page.is_exist(L.import_downloaded_media_from_cl.ok_btn, timeout=300)
            case.result = check_result
            import_media_from_cloud_page.tap_ok_btn()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        media_room_page.import_media_from_cyberlink_cloud()
        import_media_from_cloud_page.is_exist(L.import_downloaded_media_from_cl.downloaded_media_window, timeout=10)
        for check_template_ready in range(10):
            template_ready = import_media_from_cloud_page.find(
                L.import_downloaded_media_from_cl.select_deselect_all_btn, timeout=100).AXEnabled
            if not template_ready:
                time.sleep(DELAY_TIME)
                continue
            else:
                break

        import_media_from_cloud_page.switch_to_video_page()
        import_media_from_cloud_page.select_content_in_folder_level(folder_index=0, click_times=2)

        with uuid('40a95aec-4712-473b-950d-381c57815951') as case:
            # 2.3. File Level
            # 2.3.1. Search > Default text
            # show 'search the library' in the search bar
            default_text = import_media_from_cloud_page.exist(
                L.import_downloaded_media_from_cl.search_textfield).AXPlaceholderValue
            case.result = False if not default_text == 'Search the library' else True

        with uuid('f9e66da9-5c74-4d29-9975-30433c553d12') as case:
            # 2.3. File Level
            # 2.3.1. Search > Name > File Name
            # show Files with entered text
            check_result_1 = import_media_from_cloud_page.input_text_in_seacrh_library('26')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_3_1-1.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

            import_media_from_cloud_page.clear_keyword_in_search_library()

        with uuid('076a7ec1-781f-4f12-b9a5-dbbc39f163d5') as case:
            # 2.3. File Level
            # 2.3.1. Search > No search result
            # show "No clips match the search"
            check_result_1 = import_media_from_cloud_page.input_text_in_seacrh_library('xyz')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_3_1-3.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2
            import_media_from_cloud_page.tap_refresh_btn()
            import_media_from_cloud_page.select_content_in_folder_level(folder_index=0, click_times=2)

        with uuid('a87ffa4c-57b1-4480-b7d4-2875c2cd3433') as case:
            # 2.3. File Level
            # 2.3.2. [Library menu] > [Sort By] > Default
            # sort by "Upload Date"
            import_media_from_cloud_page.tap_library_menu_btn()
            import_media_from_cloud_page.tap_sort_by_item()
            default_setting = import_media_from_cloud_page.exist(
                L.import_downloaded_media_from_cl.sort_by_upload_date).AXMenuItemMarkChar
            case.result = False if not default_setting == '✓' else True

            import_media_from_cloud_page.tap_refresh_btn()

        with uuid('e01bc0fc-b7a2-4cce-b049-4b08df681f31') as case:
            # 2.3. File Level
            # 2.3.2. [Library menu] > [Sort By] > [Name]
            # can be sorted by name normally
            import_media_from_cloud_page.tap_library_menu_btn()
            import_media_from_cloud_page.tap_sort_by_item()
            check_result_1 = import_media_from_cloud_page.apply_sort_by_type(strType='Name')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_3_2-1.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('9a577c45-5a49-4633-8b2d-cce35ec98a53') as case:
            # 2.3. File Level
            # 2.3.2. [Library menu] > [Sort By] > [Size]
            # can be sorted by size normally
            import_media_from_cloud_page.tap_library_menu_btn()
            import_media_from_cloud_page.tap_sort_by_item()
            check_result_1 = import_media_from_cloud_page.apply_sort_by_type(strType='Size')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_3_2-3.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('de9dbe64-7548-4a06-a133-98c070c6410f') as case:
            # 2.3. File Level
            # 2.3.2. [Library menu] > [Sort By] > [Upload Date]
            # can be sorted by upload date normally
            import_media_from_cloud_page.tap_library_menu_btn()
            import_media_from_cloud_page.tap_sort_by_item()
            check_result_1 = import_media_from_cloud_page.apply_sort_by_type(strType='Upload Date')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_3_2-2.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('6de35a31-bc39-4837-8c6f-fe883d3697d7') as case:
            # 2.3. File Level
            # 2.3.2. [Library menu] > Icons size > Default
            # thumbnails show as medium icons
            import_media_from_cloud_page.tap_library_menu_btn()
            default_setting = import_media_from_cloud_page.exist(
                L.import_downloaded_media_from_cl.medium_icon).AXMenuItemMarkChar
            case.result = False if not default_setting == '✓' else True

            import_media_from_cloud_page.tap_refresh_btn()

        with uuid('bb12ba3f-ddff-42c3-bad5-3de752d741d2') as case:
            # 2.3. File Level
            # 2.3.2. [Library menu] > Icons size > [Extra Large Icons]
            # thumbnails show as extra large icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Extra')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_3_2-4.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('590edd57-c5d5-43af-9c84-aa72abd9f500') as case:
            # 2.3. File Level
            # 2.3.2. [Library menu] > Icons size > [Large Icons]
            # thumbnails show as large icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Large')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_3_2-5.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('c4fc5798-dc00-443a-a9cb-96db76e44c4c') as case:
            # 2.3. File Level
            # 2.3.2. [Library menu] > Icons size > [Small Icons]
            # thumbnails show as small icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Small')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_3_2-6.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('e492b64f-c165-4530-b1fd-b41fa8051912') as case:
            # 2.3. File Level
            # 2.3.2. [Library menu] > Icons size > [Medium Icons]
            # thumbnails show as medium icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Medium')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_2_3_2-7.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('ee307720-6df3-4edf-9c15-59d8323d489c') as case:
            # 2.3. File Level
            # 2.3.4. [Delete selected clips] > No files selected > Default
            # button is disabled
            button_status = import_media_from_cloud_page.exist(L.import_downloaded_media_from_cl.delete_btn).AXEnabled
            case.result = True if not button_status else False

        with uuid('83bfc213-4b09-491f-82e1-1c48a8da32c7') as case:
            # 2.3. File Level
            # 2.3.5. [Download] > No Files selected > Default
            # button is disabled
            button_status = import_media_from_cloud_page.find(L.import_downloaded_media_from_cl.download_btn).AXEnabled
            case.result = True if not button_status else False

        with uuid('cacb3631-0bc2-40ee-8c10-42b9393c8e0c') as case:
            # 2.3. File Level
            # 2.3.4. [Delete selected clips] > selected file(s)
            # button is enabled
            import_media_from_cloud_page.input_text_in_seacrh_library('H264.mp4')
            import_media_from_cloud_page.select_content_in_file_level(file_index=1)
            time.sleep(DELAY_TIME)
            button_status = import_media_from_cloud_page.exist(L.import_downloaded_media_from_cl.delete_btn).AXEnabled
            case.result = False if not button_status else True

        with uuid('2f622e55-4916-4f45-a447-28bbe6461fac') as case:
            # 2.3. File Level
            # 2.3.5. [Download] > select File(s)
            # button is enabled
            button_status = import_media_from_cloud_page.find(L.import_downloaded_media_from_cl.download_btn).AXEnabled
            case.result = False if not button_status else True

        with uuid('c04d63dd-6e38-4674-9938-4a9d7bb84cb2') as case:
            # 2.3. File Level
            # 2.3.5. [Download] > [Cancel]
            # cancel downloading
            import_media_from_cloud_page.tap_download_btn()
            check_result = import_media_from_cloud_page.tap_cancel_btn()
            case.result = check_result

        with uuid('24d06f2f-7e2e-4740-bcf4-b94f157e71cc') as case:
            # 2.3. File Level
            # 2.3.5. [Download] > Download downloaded > Dialog
            # Pop up a dialog "The clips were successfully downloaded and…".
            import_media_from_cloud_page.tap_download_btn()
            # download_from_shutterstock_page.find(L.download_from_shutterstock.download.hd_video.btn_no, timeout=100)
            # download_from_shutterstock_page.download.hd_video.click_no()
            #media_room_page.handle_high_definition_dialog()
            time.sleep(5)
            import_media_from_cloud_page.tap_ok_btn()
            time.sleep(DELAY_TIME * 5)
            import_media_from_cloud_page.tap_download_btn()
            result = False
            for x in range(150):
                if main_page.exist(L.import_downloaded_media_from_cl.ok_btn):
                    result = True
                    break
                else:
                    time.sleep(1)
            case.result = result
            import_media_from_cloud_page.tap_ok_btn()

            download_from_cl_dz_page.tap_close_button()
            time.sleep(DELAY_TIME * 2)

        with uuid('d03b8f86-8b0f-430e-96b7-70f1019c5bf1') as case:
            # 2.3. File Level
            # 2.3.5. [Download] > Complete
            # downloaded clips are available in the media library
            check_result = media_room_page.select_media_content('H264.mp4')
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        media_room_page.import_media_from_cyberlink_cloud()
        import_media_from_cloud_page.is_exist(L.import_downloaded_media_from_cl.downloaded_media_window, timeout=10)
        for check_template_ready in range(10):
            template_ready = import_media_from_cloud_page.find(
                L.import_downloaded_media_from_cl.select_deselect_all_btn, timeout=10).AXEnabled
            if not template_ready:
                time.sleep(DELAY_TIME)
                continue
            else:
                break

        import_media_from_cloud_page.switch_to_photo_page()

        with uuid('b2b3a18e-9744-4b04-8402-d63b71f42d06') as case:
            # 3. Photo
            # 3.2. Folder Level
            # 3.2.1. Search > Default text
            # show 'search the library' in the search bar
            default_text = import_media_from_cloud_page.exist(
                L.import_downloaded_media_from_cl.search_textfield).AXPlaceholderValue
            check_result = False if not default_text == 'Search the library' else True
            case.result = check_result

        with uuid('f7a106b6-690a-4535-98bd-4d13f0cc0ca0') as case:
            # 3.2. Folder Level
            # 3.2.1. Search > Name > Folder Name
            # show folders with entered text
            check_result_1 = import_media_from_cloud_page.input_text_in_seacrh_library('01')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_3_2_1-1.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

            import_media_from_cloud_page.clear_keyword_in_search_library()

        with uuid('bf61b4b1-a6d2-4627-be86-686190dc142e') as case:
            # 3.2. Folder Level
            # 3.2.1. Search > Name > File Name
            # show folders with entered text
            import_media_from_cloud_page.select_content_in_folder_level(folder_index=0, click_times=2)
            check_result_1 = import_media_from_cloud_page.input_text_in_seacrh_library('jpg')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_3_2_1-2.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2
            import_media_from_cloud_page.clear_keyword_in_search_library()
            import_media_from_cloud_page.tap_refresh_btn()

        with uuid('a3231cb9-5993-48aa-a146-10dfd79bd34d') as case:
            # 3.2. Folder Level
            # 3.2.2. [Library menu] > Icons size > Default
            # thumbnails show as medium icons
            import_media_from_cloud_page.tap_library_menu_btn()
            default_setting = import_media_from_cloud_page.exist(
                L.import_downloaded_media_from_cl.medium_icon).AXMenuItemMarkChar
            case.result = False if not default_setting == '✓' else True

            import_media_from_cloud_page.tap_refresh_btn()

        with uuid('af4898ba-febc-470e-83c8-fb0a732281c4') as case:
            # 3.2. Folder Level
            # 3.2.2. [Library menu] > Icons size > [Extra Large Icons]
            # thumbnails show as extra large icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Extra')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_3_2_2-3.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('bbfbcd2c-2455-4e1c-8d0a-69ef1dc3dd5a') as case:
            # 3.2. Folder Level
            # 3.2.2. [Library menu] > Icons size > [Large Icons]
            # thumbnails show as large icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Large')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_3_2_2-4.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('0a33f2a6-1118-43da-90e5-2566161b029a') as case:
            # 3.2. Folder Level
            # 3.2.2. [Library menu] > Icons size > [Small Icons]
            # thumbnails show as small icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Small')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_3_2_2-5.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('83855b1f-af94-4e63-a95b-a55662fcc507') as case:
            # 3.2. Folder Level
            # 3.2.2. [Library menu] > Icons size > [Medium Icons]
            # thumbnails show as medium icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Medium')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_3_2_2-6.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('0d916c4f-81ba-422b-9ce3-534860c3f508') as case:
            # 3.2. Folder Level
            # 3.2.4. [Delete selected clips] > No folders selected > Default
            # button is disabled
            button_status = import_media_from_cloud_page.find(L.import_downloaded_media_from_cl.download_btn).AXEnabled
            check_result = True if not button_status else False
            case.result = check_result

        with uuid('591713e8-6f81-442f-af63-a424518f6c0f') as case:
            # 3.2. Folder Level
            # 3.2.5. [Download] > No folders selected > Default
            # button is disabled
            button_status = import_media_from_cloud_page.find(L.import_downloaded_media_from_cl.download_btn).AXEnabled
            case.result = True if not button_status else False

        with uuid('dcb0247a-296c-4c71-a105-ea4fd0c12062') as case:
            # 3.2. Folder Level
            # 3.2.4. [Delete selected clips] > Select folder(s)
            # button is enabled
            import_media_from_cloud_page.select_content_in_folder_level(folder_index=1, click_times=1)
            time.sleep(DELAY_TIME)
            button_status = import_media_from_cloud_page.exist(L.import_downloaded_media_from_cl.delete_btn).AXEnabled
            check_result = False if not button_status else True
            case.result = check_result

        with uuid('462e5998-a093-4665-9c9b-79f2bcfdf354') as case:
            # 3.2. Folder Level
            # 3.2.5. [Download] > select folder(s)
            # button is enabled
            button_status = import_media_from_cloud_page.find(L.import_downloaded_media_from_cl.download_btn).AXEnabled
            case.result = False if not button_status else True

        with uuid('6f4577d9-ef76-47b1-a314-8189711213b2') as case:
            # 3.2. Folder Level
            # 3.2.5. [Download] > Complete > Dialog
            # Pop up a dialog "The clips are successfully downloaded and…"
            import_media_from_cloud_page.tap_download_btn()

            time.sleep(20)
            case.result = import_media_from_cloud_page.tap_ok_btn()
            time.sleep(DELAY_TIME * 5)

        with uuid('ca8752d6-e3cf-4edd-9237-8e1acb06960d') as case:
            # 3.2. Folder Level
            # 3.2.5. [Download] > Download downloaded > Dialog
            # Pop up a dialog "The clips were successfully downloaded and…".
            import_media_from_cloud_page.tap_download_btn()
            check_result = import_media_from_cloud_page.is_exist(L.import_downloaded_media_from_cl.ok_btn, timeout=150)
            case.result = check_result
            import_media_from_cloud_page.tap_ok_btn()

            download_from_cl_dz_page.tap_close_button()
            time.sleep(DELAY_TIME * 2)

        with uuid('818e1814-847f-474d-9db9-0ab0b1882777') as case:
            # 3.2. Folder Level
            # 3.2.5. [Download] > Complete
            # downloaded clips are available in the media library
            check_result = media_room_page.select_media_content('snapshot.jpg')
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        media_room_page.import_media_from_cyberlink_cloud()
        import_media_from_cloud_page.is_exist(L.import_downloaded_media_from_cl.downloaded_media_window, timeout=10)
        for check_template_ready in range(10):
            template_ready = import_media_from_cloud_page.find(
                L.import_downloaded_media_from_cl.select_deselect_all_btn, timeout=10).AXEnabled
            if not template_ready:
                time.sleep(DELAY_TIME)
                continue
            else:
                break

        import_media_from_cloud_page.switch_to_photo_page()
        import_media_from_cloud_page.select_content_in_folder_level(folder_index=0, click_times=2)
        time.sleep(DELAY_TIME * 2)

        with uuid('55d900f4-34e7-4f4e-be6b-8b367f63b917') as case:
            # 3.3. File Level
            # 3.3.1. Display > JPG
            # show thumbnail correctly
            check_result = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_3_3_1-1.png', 'Download Media Window')
            case.result = check_result

        with uuid('d619f9b2-c126-4f5e-8f6c-a45384d72ed9') as case:
            # 3.3. File Level
            # 3.3.1. Display > BMP
            # show thumbnail correctly
            case.result = check_result

        with uuid('379ca78e-f7a2-4073-a840-27b91330694e') as case:
            # 3.3. File Level
            # 3.3.1. Display > PNG w/ alpha
            # show thumbnail correctly
            case.result = check_result

        with uuid('a35eb30a-df62-43f3-9dd8-41c97dd98d0d') as case:
            # 3.3. File Level
            # 3.3.2. Search > Default text
            # show 'search the library' in the search bar
            default_text = import_media_from_cloud_page.exist(
                L.import_downloaded_media_from_cl.search_textfield).AXPlaceholderValue
            case.result = False if not default_text == 'Search the library' else True

        with uuid('bc61bd19-0c43-491f-9dc2-682eee0b850c') as case:
            # 3.3. File Level
            # 3.3.2. Search > Name > File Name
            # show Files with entered text
            check_result_1 = import_media_from_cloud_page.input_text_in_seacrh_library('jpg')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_3_3_2-1.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2
            import_media_from_cloud_page.clear_keyword_in_search_library()

        with uuid('0508e84a-839f-47ac-a554-b1441ed04a73') as case:
            # 3.3. File Level
            # 3.3.6. [Download] > No Files selected > Default
            # button is disabled
            button_status = import_media_from_cloud_page.find(L.import_downloaded_media_from_cl.download_btn).AXEnabled
            case.result = True if not button_status else False

        with uuid('e7eb5c03-0361-44d5-9955-2e4ba2691e3b') as case:
            # 3.3. File Level
            # 3.3.6. [Download] > select File(s)
            # button is enabled
            import_media_from_cloud_page.select_content_in_file_level(file_index=5)
            time.sleep(DELAY_TIME)
            button_status = import_media_from_cloud_page.find(L.import_downloaded_media_from_cl.download_btn).AXEnabled
            case.result = False if not button_status else True

        with uuid('913dad65-cef3-4846-84d4-715b9621760a') as case:
            # 3.3. File Level
            # 3.3.6. [Download] > Complete > Dialog
            # Pop up a dialog "The clips are successfully downloaded and..."
            import_media_from_cloud_page.tap_download_btn()
            time.sleep(20)
            case.result = import_media_from_cloud_page.tap_ok_btn()
            time.sleep(DELAY_TIME * 10)

        with uuid('9404566a-3f0e-449c-9547-123880494bf6') as case:
            # 3.3. File Level
            # 3.3.6. [Download] > Download downloaded > Dialog
            # Pop up a dialog "The clips were successfully downloaded and…".
            import_media_from_cloud_page.tap_download_btn()
            time.sleep(DELAY_TIME * 3)
            check_result = import_media_from_cloud_page.is_exist(L.import_downloaded_media_from_cl.ok_btn, timeout=150)
            case.result = check_result
            import_media_from_cloud_page.tap_ok_btn()

            download_from_cl_dz_page.tap_close_button()
            time.sleep(DELAY_TIME * 2)

        with uuid('4278392e-79c5-41ad-88e0-c7b22cade051') as case:
            # 3.3. File Level
            # 3.3.6. [Download] > Complete
            # downloaded clips are available in the media library
            check_result = media_room_page.select_media_content('lake_001.jpg')
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        media_room_page.import_media_from_cyberlink_cloud()
        import_media_from_cloud_page.is_exist(L.import_downloaded_media_from_cl.downloaded_media_window, timeout=10)
        for check_template_ready in range(10):
            template_ready = import_media_from_cloud_page.find(
                L.import_downloaded_media_from_cl.select_deselect_all_btn, timeout=10).AXEnabled
            if not template_ready:
                time.sleep(DELAY_TIME)
                continue
            else:
                break

        import_media_from_cloud_page.switch_to_music_page()
        time.sleep(DELAY_TIME)

        with uuid('48e5a2a7-e37f-4f58-9bfc-ec1b92575728') as case:
            # 4. Music
            # 4.2. Folder Level
            # 4.2.5. [Download] > Complete > Dialog
            # Pop up a dialog "The clips are successfully downloaded and…"
            import_media_from_cloud_page.select_content_in_folder_level(folder_index=0, click_times=1)
            import_media_from_cloud_page.tap_download_btn()

            time.sleep(20)
            case.result = import_media_from_cloud_page.tap_ok_btn()
            time.sleep(DELAY_TIME * 5)

        with uuid('8c1f8e93-5170-4319-bcc8-c82ff257962b') as case:
            # 4.2. Folder Level
            # 4.2.5. [Download] > Download downloaded > Dialog
            # Pop up a dialog "The clips were successfully downloaded and…"
            import_media_from_cloud_page.tap_download_btn()
            check_result = import_media_from_cloud_page.is_exist(L.import_downloaded_media_from_cl.ok_btn, timeout=150)
            case.result = check_result
            import_media_from_cloud_page.tap_ok_btn()

            download_from_cl_dz_page.tap_close_button()
            time.sleep(DELAY_TIME * 2)

        with uuid('3bc2eda0-38d5-4547-a20f-30d76657715b') as case:
            # 4.2. Folder Level
            # 4.2.5. [Download] > Complete
            # Downloaded clips are available in the media library
            check_result = media_room_page.select_media_content('sample4.mp3')
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        media_room_page.import_media_from_cyberlink_cloud()
        import_media_from_cloud_page.is_exist(L.import_downloaded_media_from_cl.downloaded_media_window, timeout=10)
        for check_template_ready in range(10):
            template_ready = import_media_from_cloud_page.find(
                L.import_downloaded_media_from_cl.select_deselect_all_btn, timeout=10).AXEnabled
            if not template_ready:
                time.sleep(DELAY_TIME)
                continue
            else:
                break

        import_media_from_cloud_page.switch_to_music_page()
        import_media_from_cloud_page.select_content_in_folder_level(folder_index=0, click_times=2)
        time.sleep(DELAY_TIME * 2)

        with uuid('9d153a98-36b0-43b3-8edf-9474ffd14b08') as case:
            # 4. Music
            # 4.1. General Function
            # 4.1.1. Display > AAC
            # show thumbnail correctly
            check_result = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_4_1_1-1.png', 'Download Media Window')
            case.result = check_result

        with uuid('c47d32b6-a1fe-499a-af75-044da94e8abd') as case:
            # 4.1. General Function
            # 4.1.1. Display > FLAC
            # show thumbnail correctly
            case.result = check_result

        with uuid('f14eb92b-6ed4-4206-8fc6-74e13b0c0864') as case:
            # 4.1. General Function
            # 4.1.1. Display > M4A
            # show thumbnail correctly
            case.result = check_result

        with uuid('75f2d643-653b-46f8-948f-e9bbe9a5d72b') as case:
            # 4.1. General Function
            # 4.1.1. Display > WAV
            # show thumbnail correctly
            case.result = check_result

        with uuid('f7adb6cd-188b-43c6-8008-cdf30939bead') as case:
            # 4.1. General Function
            # 4.1.1. Display > MP3
            # show thumbnail correctly
            case.result = check_result

        with uuid('127e5d7c-bba0-406f-b160-4063e6f8dc62') as case:
            # 4.3. File Level
            # 4.3.2. [Library menu] > [Sort By] > Default
            # short by " Upload Date"
            import_media_from_cloud_page.tap_library_menu_btn()
            import_media_from_cloud_page.tap_sort_by_item()
            default_setting = import_media_from_cloud_page.exist(
                L.import_downloaded_media_from_cl.sort_by_upload_date).AXMenuItemMarkChar
            case.result = False if not default_setting == '✓' else True

            import_media_from_cloud_page.tap_refresh_btn()

        with uuid('5a45389f-3c5f-4a92-8c12-587cb12131a4') as case:
            # 4.3. File Level
            # 4.3.2. [Library menu] > [Sort By] > [Name]
            # can be sorted by name normally
            import_media_from_cloud_page.tap_library_menu_btn()
            import_media_from_cloud_page.tap_sort_by_item()
            check_result_1 = import_media_from_cloud_page.apply_sort_by_type(strType='Name')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_4_3_2-1.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('6fe009b6-0d82-4052-a7dc-c7ab151c1c79') as case:
            # 4.3. File Level
            # 4.3.2. [Library menu] > [Sort By] > [Size]
            # can be sorted by size normally
            import_media_from_cloud_page.tap_library_menu_btn()
            import_media_from_cloud_page.tap_sort_by_item()
            check_result_1 = import_media_from_cloud_page.apply_sort_by_type(strType='Size')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_4_3_2-3.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('ef71a4f5-a98e-4b03-b62f-27ee1d2fee4c') as case:
            # 4.3. File Level
            # 4.3.2. [Library menu] > [Sort By] > [Upload Date]
            # can be sorted by upload date normally
            import_media_from_cloud_page.tap_library_menu_btn()
            import_media_from_cloud_page.tap_sort_by_item()
            check_result_1 = import_media_from_cloud_page.apply_sort_by_type(strType='Upload Date')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_4_3_2-2.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('003b9e62-a663-4ab2-8734-f158bec456e1') as case:
            # 4.3. File Level
            # 4.3.2. [Library menu] > Icon size > Default
            # thumbnail show as medium icons
            import_media_from_cloud_page.tap_library_menu_btn()
            default_setting = import_media_from_cloud_page.exist(
                L.import_downloaded_media_from_cl.medium_icon).AXMenuItemMarkChar
            case.result = False if not default_setting == '✓' else True

            import_media_from_cloud_page.tap_refresh_btn()

        with uuid('6df056c7-42f5-4122-b43b-08422d7db3c8') as case:
            # 4.3. File Level
            # 4.3.2. [Library menu] > Icon size > [Extra Large Icons]
            # thumbnail show as extra large icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Extra')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_4_3_2-4.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('0c78b082-19d3-469b-8716-8418d3b16c7b') as case:
            # 4.3. File Level
            # 4.3.2. [Library menu] > Icon size > [Large Icons]
            # thumbnail show as large icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Large')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_4_3_2-5.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('6a3907fe-33e1-4d14-bec1-6798e339d42a') as case:
            # 4.3. File Level
            # 4.3.2. [Library menu] > Icon size > [Small Icons]
            # thumbnail show as small icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Small')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_4_3_2-6.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('d8b7f6f8-6285-4862-b0f6-d56f467a281e') as case:
            # 4.3. File Level
            # 4.3.2. [Library menu] > Icon size > [Medium Icons]
            # thumbnail show as medium icons
            import_media_from_cloud_page.tap_library_menu_btn()
            check_result_1 = import_media_from_cloud_page.set_icon_size(strType='Medium')
            check_result_2 = import_media_from_cloud_page.check_downloaded_media_preview(
                Ground_Truth_Folder + 'import_media_from_cloud_4_3_2-7.png', 'Download Media Window')

            case.result = check_result_1 and check_result_2

        with uuid('320f7dfc-bc30-44cb-834c-f211edb141c1') as case:
            # 4.3. File Level
            # 4.3.5. [Download] > Complete > Dialog
            # Pop up a dialog "The clips are successfully downloaded and…"
            import_media_from_cloud_page.select_content_in_file_level(file_index=3)
            time.sleep(DELAY_TIME)

            import_media_from_cloud_page.tap_download_btn()
            time.sleep(30)
            case.result = import_media_from_cloud_page.tap_ok_btn()
            time.sleep(DELAY_TIME * 5)

        with uuid('a864c87f-796c-4d11-a540-2694dcdbd8c8') as case:
            # 4.3. File Level
            # 4.3.5. [Download] > Download downloaded > Dialog
            # Pop up a dialog "The clips were successfully downloaded and…"
            import_media_from_cloud_page.tap_download_btn()
            case.result = import_media_from_cloud_page.tap_ok_btn()
            download_from_cl_dz_page.tap_close_button()
            time.sleep(DELAY_TIME * 2)

        with uuid('91d18733-ceec-46d3-94cf-6ec2b93579a8') as case:
            # 4.3. File Level
            # 4.3.5. [Download] > Complete
            # Downloaded clips are available in the media library
            check_result = media_room_page.select_media_content('sample4.mp3')
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    66510466-9604-405a-b7a5-0f6ae91b5c46
                    c1953c8f-7d95-413d-9980-4d165cd543e5
                    6eca6945-559d-4d95-bb94-6ad822c6f2ab
                    3f3bf045-2e9e-4bf4-9054-c85226903e7c
                    c0da69b0-52cc-4529-ba32-deb0ec44d173
                    efb57b76-f97a-47eb-ab08-b9c0a230b795
                    0610bfa9-86b3-4ecd-82ed-da6e77fe4300
                    d3f5c656-afca-4eb9-afcf-937f1095c3d4
                    df9e6a79-4a1c-4985-822d-9a13dffaffb0
                    bccf5ba4-891d-4094-b4be-f7a2b86e8eff
                    8158107c-de33-4e61-b4c5-b3cab1d66001
                    18e1c9b3-f845-462d-b1cc-536d6ed69d7a
                    cc0cf98e-fe07-43c3-83c2-72308b6eebee
                    401c686d-0971-4f90-aabf-006195063946
                    8c408ca0-6398-4cf6-8e10-4d591d9c045f
                    ddb298f5-d43c-4aab-9d07-0141a63585be
                    dc68b80c-2c05-49a9-b85c-886e92f26fd2
                    da4aeac2-790d-4a21-9a82-9f0db385f16d
                    7f6588f3-c662-4da5-81b0-cedc884a5be0
                    11652744-14e0-4510-98a3-cac71f4008fb
                    dba2e3e2-0be3-40a1-a173-d93d7cc7f3a4
                    ad1ef5f7-021e-4c0c-a334-7714fc5e67c0
                    ca7828df-8641-4534-8ab4-4239e490a433
                    a0a36ccd-649e-4ee5-90ab-8bbc613141d7
                    ace5e66d-1ebb-40c4-92e2-4d729bc56b70
                    15adf74e-9752-491b-ba73-1697b8bf5714
                    eff7dbe0-39f6-4c9a-ac6e-f02ee512036f
                    69d443d7-cd19-46ad-8829-061a31f1018c
                    cc845816-7297-4227-a242-99df794cf5e3
                    af9e0788-7a17-4034-a0a6-72dbf83481eb
                    f2272f6a-acac-4469-8793-fa154ea39096
                    5b480b02-0ffa-4910-818f-b3dd4c42c420
                    364edfcf-4a86-4c0a-b8a6-e46d74494b38
                    fa16c504-1210-4c3b-a332-9d9a3c7dbaae
                    028e9be1-71fe-400c-a976-362a0e72fd60
                    719b4a1e-75e2-42f3-9f82-c04fb9e73eaa
                    3e4f7c45-19b2-4b2b-8065-85abdb966d8f
                    f89dcd3d-00ec-4a0f-86ac-a02bd6747098
                    da0389a8-ea41-4678-abcb-1919d91b8fbe
                    a7ef2c83-7f00-4156-acc3-e6fa4ac40afc
                    e8d42b19-e3bd-49b6-95f1-0e1f1a3b8283
                    0c4984f3-359f-45fc-9fdc-df220411e127
                    89abc5a3-9640-47ad-8492-e841d45a70d1
                    94d96998-99ff-4863-a488-ecd85775e748
                    9756be86-a1d7-4344-b57e-db3117ec808a
                    617ebff2-323e-48ec-a461-847bcf72d43d
                    e6a3e4a5-fee1-45c6-9187-a933d54e186e
                    4c261e02-0a9a-4904-a033-4fe2afd71d0e
                    28feb635-75fb-48c4-8569-633227647764
                    521041bc-7988-46ae-9a46-791e1ce07391
                    d880d2e8-eddf-45ce-ae8b-d5528d5ed62f
                    f24e7074-1f6a-4e3d-bfb0-71cd0bac3d2d
                    abcb7ef7-6192-4165-97eb-c422d50cc35f
                    16794781-95d3-4837-a968-f2f7d15c8686
                    becbbf8d-d6ab-476b-9b14-bd7c99314515
                    1be466e2-a402-4a71-af2c-9e5b16665515
                    410a6fbc-6460-4af0-a62c-c1d2cfb476c3
                    a49e760c-9c68-4a07-b068-1581b0b7c301
                    4a9596fe-bfd6-4113-8d10-ee68bfbf17d2
                    5152dff0-f94a-4ed2-82d7-3650cf4ad2fd
                    f8cfc00f-e66c-45d9-9dbd-6db16a3d7d54
                    de1fda60-9f37-47bf-a272-1d31e7f3171e
                    5e760305-66b4-4175-b99a-570797edeebd
                    919ffb2f-5bab-48dc-b946-bfbd0ebf0404
                    f161d5e6-14a5-45d6-b43e-1010a7e0fce5
                    cd749f74-b241-4083-a55b-bc0d712cd9ee
                    495f5a00-a23a-4411-b71c-1bc1abbbc2e9
                    2ce4cc06-831a-48b0-9597-6a667eb2c445
                    aba3cd36-559e-4498-a1e4-097f8f9c08f9
                    89f55117-ffd2-4c74-8093-dbe94e477adc
                    272f59f6-6bf7-4205-907c-076cd3689bd3
                    496ce250-8158-4b52-a46b-7a9d9b18ebeb
                    923e8c1b-c75a-4dc8-8075-6d8dcce49b48
                    a9d0f764-25d6-4aa0-88d0-ab616e869b21
                    9dc9f807-f482-4609-88ce-29805ba72ab9
                    4595975c-6213-43af-bd73-4faaa44da463
                    91435a77-b479-4dce-89da-e7f22725ba95
                    02dd4379-ec65-4a1d-aedd-f7f4e2657147
                    51d17646-1ebe-4867-88f7-afff6e50ba87
                    4ea3d8a8-c858-44ac-bfc5-7836d214bb06
                    7c03df09-ae65-4337-99ff-2347414361a0
                    ea29e284-24f8-4a15-b2c7-baffc6783daf
                    dbfa9a25-7d75-4e8c-b00e-b821af0fb82a
                    773d331d-86e7-4676-b63e-ffea3a6de511
                    ae64b27a-280e-4c76-9b0c-b1959772744b
                    adb33411-7e78-4bd9-8791-b3a4d628a9cd
                    d9e57e6e-69fd-4885-b3dd-f7e8845fc306
                    84c22117-75c5-4c2c-887a-1e8dc266842b
                    5330ab59-0769-45b8-98c5-5a9562bc744a
                    23ed6c7d-bde4-4234-a37f-1b998839b4ea
                    b98da297-a9ac-4415-9ee0-20a7c1bb92b1
                    f25e9ac1-cbdc-4bc5-a444-3d6bc69ba145
                    b3b2d40b-279c-490d-9cea-730390f3b493
                    b25abd06-8169-4a08-a3ca-b04701b3ce03
                    35410d4c-391a-49ed-b084-9019fd9021fc
                    a1ec2353-2622-4353-807e-f92b3a5b735a
                    6796059b-ee5a-49f7-8ac1-040d0b7c4217
                    455f1508-74a1-4097-99fe-dcf0bececef4
                    0b85237b-a9bc-4278-a95a-4a3bc8d36b30
                    bb09630b-ef0b-4b7c-acd7-084714609d5a
                    631311e3-842a-4bcc-9d49-0aa4159f9012
                    ab77c16b-0e6e-4916-8acc-8ede75c655e5
                    33a35768-33fa-468f-b9d1-a3ac140f39b0
                    dbf08e4d-f32f-4850-a104-5d4caa79764d
                    22523699-332f-44ff-a3bf-209251c945de
                    6ce68f2a-8981-4b60-87da-db47a5a60625
                    fdfc215f-6eaf-487e-8971-20a142ebca21
                    3b042ff1-6264-42f4-80b1-72ff563383a8
                    cd5f464a-edde-4df3-aec7-770ed9be0589
                    606d8d79-9e3d-4b46-b567-c83600dc8ae9
                    fd18c7d8-3be8-49cc-b0f7-a555963760e9
                    296c33cd-7cac-4efb-9394-988b026aa3fc
                    40f01f3e-767c-4b1a-b585-8ad5ce08daa3
                    4444377b-48ae-4572-a117-1db6d1849147
                    b4f8d802-7ba7-4a77-b929-431c365a1f0b
                    3d0e3888-30cf-4891-9a5a-da1033a21e21
                    357b835a-5667-4fcf-8429-1d4e3af8671c
                    a9f3a345-5434-47ed-a36a-289ce1ae7565
                    21c4ad9b-0d84-4790-acfb-8c72a48c78b1
                    b999dc60-acd4-4c72-b285-7791582cd7c0
                    1e2fd9d1-da09-44c4-b384-8f4f340d0c84
                    2a6bae33-85aa-43eb-a31b-4b6b6ed10143
                    08afa494-eca3-4505-a5ea-6124c1dd8227
                    06b427ec-c75e-4ab6-aba8-e6bf26a33217
                    c467dae0-8aaa-489c-b566-c3d12222c62b
                    882ac514-9d62-4af1-87ad-b264295dcae4
                    95686111-bd1b-4df4-93e9-150227960e2a
                    8b7431af-7bdd-490b-9f52-99eab0433c1a
                    bcc6e7db-b9a1-4d5d-bcac-772e2e5bbd0e
                    2e4847e7-f3dc-4d7a-b828-60c81af02ab9
                    10a22cb7-363c-4079-af47-2f883e089d23
                    a09fa89d-7afb-46a9-aad5-299f0aa59206
                    e0bcab51-7775-49cd-84be-30d4539df3f9
                    931b3a55-78d3-4ffa-8071-98fdac8def65
                    e8f05cb8-fa99-480f-868f-5697bfc861a0
                    80f7f685-12dc-47ea-ac07-0e4a622a5a6c
                    78d431d6-8b00-4363-99d3-1cae31ecbd88
                    e86ee4cf-4dec-4b61-8f62-cb5fa05b4749
                    a43c9d27-ac2d-4028-aa32-43702dab8bc1
                    98194af8-86fa-4943-b740-6e71390e1e4d
                    1f42da8e-4249-4131-98a6-88e7da35ed16
                    80db93ae-9be8-4bc1-abf3-b810573d2de6
                    bea5d8a0-ca5a-411d-a3f0-24bacc2ab00f
                    b8327b2b-51fe-4b21-80d6-9cc4dc8c99af
                    2ee2d25f-584c-4b31-9271-fce03073d480
                    e6639100-8a82-4857-9fa9-08982d80827d
                    f25e894e-c180-4ac0-96f6-99a595bdbb5b
                    5089af8a-95e8-4a33-b62f-865861e2e904
                    dfeaf57e-de3b-435c-bd80-417c0583885c
                    20487a04-1308-4e22-802d-f264851a35d4
                    e634d829-49ab-4154-8219-7a2a28bdbbab
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'





