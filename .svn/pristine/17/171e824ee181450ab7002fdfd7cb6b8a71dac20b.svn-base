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
download_from_shutterstock_page = PageFactory().get_page_object('download_from_shutterstock_page', mwc)
preferences_page = PageFactory().get_page_object('preferences_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
gettyimage_page = PageFactory().get_page_object('gettyimage_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="ShutterStock.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Download_From_Shutterstock/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Download_From_Shutterstock/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Download_From_Shutterstock():
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
            google_sheet_execution_log_init('Download_From_Shutterstock')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"download from shutterstock result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        with uuid('29572788-612f-40e2-b534-e8c377546592') as case:
            # 1. General
            # 1.1 Entrance
            # 1.1.1. Import Media bar > [Import media]>[Download Media from Shutterstock]
            # pop up the download media from shutterstock window
            media_room_page.import_media_from_shutterstock()
            time.sleep(4)
            gettyimage_page.switch_to_SS()
            time.sleep(4)
            case.result = download_from_shutterstock_page.is_in_shutterstock()
            download_from_shutterstock_page.switch_to_video()

        with uuid('dc461201-dea2-45f8-b55f-fa54e1a31bf9') as case:
            # 1.6. Scroll bar
            # 1.6.1. Default status
            # enable scroll bar
            case.result = download_from_shutterstock_page.is_exist(L.download_from_shutterstock.scroll_media)

        with uuid('003a4b46-8429-4a63-ac95-ecee49a9d58f') as case:
            # 1.2. Caption Bar
            # 1.2.1. General Functions > [x] > Close
            # close the download media from shutterstock window
            download_from_shutterstock_page.click_close()
            time.sleep(DELAY_TIME)
            case.result = not (download_from_shutterstock_page.is_in_shutterstock())

        with uuid('864c0de0-a2d3-4af6-8a92-454e4a5d6bf3') as case:
            # 1.1 Entrance
            # 1.1.2. Right click on space place > [Download From]>[Download Media from Shutterstock]
            # pop up the download media from shutterstock window
            media_room_page.collection_view_deselected_media()
            time.sleep(DELAY_TIME)
            media_room_page.right_click()
            time.sleep(DELAY_TIME)
            media_room_page.select_right_click_menu(
                'Download from', 'Download Media from Shutterstock and Getty Images...')
            case.result = download_from_shutterstock_page.is_in_shutterstock()

            time.sleep(DELAY_TIME * 8)  # waiting for all clips index ready

        with uuid('8850210c-5fc9-44bd-889d-69d9cf129bde') as case:
            # 1.2. Caption Bar
            # 1.2.1. General Functions > [Maximize] Button > Maximize
            # maximize the download media from shutterstock window
            download_from_shutterstock_page.click_maximize()
            time.sleep(DELAY_TIME)

            # check thumbnail amount == 45
            result = download_from_shutterstock_page.video.check_this_page_thumbnail_amount()
            if result != 45:
                case.result = False
            else:
                case.result = True
            ''' 
            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_1_2_1_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_1_2_1_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview)
            '''
        with uuid('7c88b979-e4d5-431e-9375-a0003bd24b35') as case:
            # 1.2. Caption Bar
            # 1.2.1. General Functions > [Restore down] Button > Restore down
            # restore down the download media from shutterstock window
            download_from_shutterstock_page.click_maximize()
            time.sleep(DELAY_TIME)

            # check thumbnail amount == 12
            result = download_from_shutterstock_page.video.check_this_page_thumbnail_amount()
            if result != 12:
                case.result = False
            else:
                case.result = True

        with uuid('2cc86c62-f652-480d-a15b-722cb555b167') as case:
            # 1.2. Caption Bar
            # 1.2.2. Caption Name > Download Media from Shutterstock
            # display "Download Media from Shutterstock" on the caption bar
            caption_title_text = download_from_shutterstock_page.get_caption_title()
            case.result = False if not caption_title_text == 'Download Media from Shutterstock and Getty Images' \
                else True

        with uuid('5a10a16e-b697-4f2d-aade-ef865778f5e0') as case:
            # 1.4. Preview
            # 1.4.1. Thumbnail > Default thumbnail (From Other Entrance)
            # check(Video/Photo) thumbnail preview gray, black or not
            download_from_shutterstock_page.switch_to_photo()
            time.sleep(6)
            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_1_4_1_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_1_4_1_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            check_result_1 = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.85)

            download_from_shutterstock_page.switch_to_video()

            # check thumbnail amount == 12
            result = download_from_shutterstock_page.video.check_this_page_thumbnail_amount()
            logger(result)
            if result != 12:
                check_thumbnail_amount = False
            else:
                check_thumbnail_amount = True

            case.result = check_result_1 and check_thumbnail_amount

            ''' 
            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_1_4_1_2.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_1_4_1_2.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            check_result_2 = download_from_shutterstock_page.compare(ground_truth, current_preview)
            '''

        with uuid('11af3b43-5262-441e-9f9d-9e66a5f4895b') as case:
            # 1.4. Preview
            # 1.4.2. Preview icon
            # check(Video/Photo) preview icon truncate or not
            case.result = check_result_1 and check_thumbnail_amount

        with uuid('7b121f0b-63f2-4534-9a7d-8f261e24f4ae') as case:
            # 1.5. [i] button
            # 1.5.1. [i] button > icons
            # exist(i button) in below
            case.result = download_from_shutterstock_page.is_exist(L.download_from_shutterstock.btn_i)

        with uuid('0790194b-6212-4e22-a77d-a5f55262690b') as case:
            # 1.5. [i] button
            # 1.5.1. [i] button > Tooltip
            # exist(i button) tooltip
            download_from_shutterstock_page.hover_i_button()
            time.sleep(DELAY_TIME * 5)
            case.result = download_from_shutterstock_page.verify_i_tooltip(
                file_name=Ground_Truth_Folder + 'shutterstock_1_5_1_1.png')

        with uuid('2ff39758-189b-48cb-8117-09989e304c58') as case:
            # 1.5. [i] button
            # 1.5.2. Terms of Use > Click [i] button > Pop up(Terms of Use)
            # list all information about(terms of use)
            # for saving space, the dialog shows the video & photo parts only;
            # in Music tab, the dialog shows music part only
            download_from_shutterstock_page.click_i_button()
            case.result = download_from_shutterstock_page.verify_i_dialog()
            time.sleep(DELAY_TIME)
            download_from_shutterstock_page.close_i_dialog()

        with uuid('6bd1b71f-0237-48ca-ac70-3b35e92270b3') as case:
            # 1.7. Previous/Next Page
            # 1.7.1. Next Page > Tooltip
            # next page
            download_from_shutterstock_page.hover_next_page()
            time.sleep(DELAY_TIME * 2)
            case.result = download_from_shutterstock_page.verify_next_page_tooltip(
                ground_truth=Ground_Truth_Folder + 'shutterstock_1_7_1_1.png')

        with uuid('9d373d35-b825-4da3-81a8-1e8f55721ead') as case:
            # 1.7. Previous/Next Page
            # 1.7.1. Next Page > Next Page > button
            # go to next page if click ">" button
            download_from_shutterstock_page.click_next_page()

            if download_from_shutterstock_page.Check_PreviewWindow_is_different(area=L.download_from_shutterstock.frame_scroll_view, sec=2):
                check_thumbnail_content = True
            else:
                check_thumbnail_content = False

            # check thumbnail amount == 12
            result = download_from_shutterstock_page.video.check_this_page_thumbnail_amount()
            if result != 12:
                check_thumbnail_amount = False
            else:
                check_thumbnail_amount = True

            case.result = check_thumbnail_content and check_thumbnail_amount
            ''' 
            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_1_7_1_2.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_1_7_1_2.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview)
            '''
        with uuid('43ac7c4f-e959-422e-a1aa-da316f75598d') as case:
            # 1.7. Previous/Next Page
            # 1.7.2. Previous Page > Tooltip
            # previous page
            download_from_shutterstock_page.hover_previous_page()
            time.sleep(DELAY_TIME * 2)
            case.result = download_from_shutterstock_page.verify_previous_page_tooltip(
                ground_truth=Ground_Truth_Folder + 'shutterstock_1_7_2_1.png')

        with uuid('e6986976-e11a-48d9-8e18-bae7057c18b6') as case:
            # 1.7. Previous/Next Page
            # 1.7.2. Previous Page > Previous Page > button
            # go to previous page if click "<" button
            download_from_shutterstock_page.click_previous_page()

            if download_from_shutterstock_page.Check_PreviewWindow_is_different(area=L.download_from_shutterstock.frame_scroll_view, sec=2):
                check_thumbnail_content = True
            else:
                check_thumbnail_content = False

            # check thumbnail amount == 12
            result = download_from_shutterstock_page.video.check_this_page_thumbnail_amount()
            if result != 12:
                check_thumbnail_amount = False
            else:
                check_thumbnail_amount = True

            case.result = check_thumbnail_content and check_thumbnail_amount
            '''
            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_1_7_2_2.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_1_7_2_2.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview)
            '''
        with uuid('3a2313a5-fa47-47c1-b4d4-e3bc66145b1f') as case:
            # 1.2. Caption Bar
            # 1.2.1. General Functions > [Esc] > Hotkey
            # close the download media from shutterstock window
            download_from_shutterstock_page.press_esc_key()  # unselect on search box
            download_from_shutterstock_page.press_esc_key()
            time.sleep(DELAY_TIME)
            case.result = not (download_from_shutterstock_page.is_in_shutterstock())

        with uuid('f82143dc-11d4-45bc-b5e7-81c9dd2c757e') as case:
            # 1.1 Entrance
            # 1.1.3. Media Room > [Premium Media]
            # pop up the download media from shutterstock window
            media_room_page.hover_library_media('Stock Content')
            time.sleep(DELAY_TIME)
            media_room_page.double_click()
            case.result = download_from_shutterstock_page.is_in_shutterstock()

            time.sleep(DELAY_TIME * 8)  # waiting for all clips index ready

        with uuid('2ac7db60-e521-43be-977f-49f989996c06') as case:
            # 1.2. Caption Bar
            # 1.2.1. General Functions > Adjust window size
            # resize by dragging the window
            download_from_shutterstock_page.adjust_window(x=325, y=61, w=949, h=747)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_1_2_1_3.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_1_2_1_3.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.8)

        with uuid('740965c4-6eb1-46a0-9e71-85f94c71576a') as case:
            # 1.6. Scroll bar
            # 1.6.2. Check scroll bar > Adjust windows size
            # resize the window then check scroll bar status
            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_1_6_2_2.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_1_6_2_2.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.scroll_media, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview)

        with uuid('793671e6-441f-4b41-aa7c-e95974b6811c') as case:
            # 1.2. Caption Bar
            # 1.2.1. General Functions > Adjust window size then close > Open again
            # reopen to keep the previous size
            download_from_shutterstock_page.click_close()
            time.sleep(DELAY_TIME)
            media_room_page.import_media_from_shutterstock()
            time.sleep(DELAY_TIME * 8)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_1_2_1_4.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_1_2_1_4.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.8)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid('a13d29cd-d1d3-45f6-9129-e773f5387534') as case:
            # 2. Video
            # 2.1. Before Search
            # 2.1.1. Search box > Default text
            # show "search" / empty in the search box
            media_room_page.import_media_from_shutterstock()
            time.sleep(10)
            gettyimage_page.switch_to_SS()
            time.sleep(4)
            download_from_shutterstock_page.switch_to_video()
            # waiting for shutterstock ready
            download_from_shutterstock_page.is_exist(L.download_from_shutterstock.frame_clips, timeout=10)
            case.result = download_from_shutterstock_page.search.verify_default_string(default='Search')

            time.sleep(DELAY_TIME * 8)

        with uuid('b15b28aa-7b16-4be8-a0b5-4934716661ca') as case:
            # 2.1. Before Search
            # 2.1.1. Search box > Tooltip
            # show "Search"
            case.result = download_from_shutterstock_page.search.verify_tooltip(
                Ground_Truth_Folder + 'shutterstock_2_1_1_1.png')

        with uuid('b56af15d-9acb-41aa-b60c-4f41d2f9af50') as case:
            # 2.1. Before Search
            # 2.1.2. Library menu > Default Icons size > [Medium icons]
            # thumbnails show as medium icons. one page has 30 icons
            current_setting = download_from_shutterstock_page.get_library_setting()
            logger(current_setting)
            check_result_1 = False if not current_setting == 'Medium' else True

            download_from_shutterstock_page.video.hover_thumbnail(index=0)
            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result_2 = False if not clip_number == 12 else True

            case.result = check_result_1 and check_result_2

        with uuid('c5588705-1ebd-4e72-be1e-06b377cda88d') as case:
            # 2.1. Before Search
            # 2.1.3. Page number > Current Page number
            # default value is "1"
            current_page_amount = download_from_shutterstock_page.get_page_amount()
            case.result = False if not current_page_amount == 1 else True

        with uuid('5f1a3852-aeb1-4964-ad77-4960f7bc1e98') as case:
            # 2.1. Before Search
            # 2.1.3. Page number > Total Page number
            # total page number
            # Due to add filter feature (VDE213508-0010), total page number is changed to 125
            # 20.7.4210: One page has 100 content (VVIP request)
            total_page_amount = download_from_shutterstock_page.get_total_page_amount()
            logger(total_page_amount)
            case.result = False if not total_page_amount == 38 else True

        with uuid('8f483177-c467-47de-bcb1-24f822df343a') as case:
            # 2.1. Before Search
            # 2.1.4. [Download] > Default status
            # button is disable
            button_status = download_from_shutterstock_page.is_enabled_download()
            case.result = True if not button_status else False

        with uuid('82012785-74db-4074-93fa-caba4e455aab') as case:
            # 2.1. Before Search
            # 2.1.4. [Download] > Tooltip
            # show "Download"
            case.result = download_from_shutterstock_page.verify_download_tooltip(
                Ground_Truth_Folder + 'shutterstock_2_1_4_1.png')

        with uuid('401a1340-aac1-4c59-96ca-8e0716641a2e') as case:
            # 2.1. Before Search
            # 2.1.5. Selected clip(s) > Default value
            # show "0 clips"
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            case.result = False if not selected_amount == 0 else True

        with uuid('2cfbb36d-c820-4db0-a890-7041739cd738') as case:
            # 2.2. After Search
            # 2.2.1. Search box > input keyword
            # show the string which is user keyin
            download_from_shutterstock_page.search.search_text('pink ball play')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'pink ball play' else True

            time.sleep(DELAY_TIME * 8)
            download_from_shutterstock_page.set_scroll_bar(0)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_2_1_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_2_1_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            check_result_2 = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.7)

            case.result = check_result_1 and check_result_2

        with uuid('7342474a-a8aa-45b6-9a23-241e90bc3fc7') as case:
            # 2.2. After Search
            # 2.2.2. Page number > Input page number > input box
            # check current page and library panel is updated to user keyin number
            download_from_shutterstock_page.page_number.set_value('3')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=10)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_2_2_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_2_2_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.7)

        with uuid('af89d3ff-745e-4a8f-ac32-c3e7cbc3b647') as case:
            # 2.2. After Search
            # 2.2.2. Page number > Current Page number
            # update current page if click [next/previous] page
            download_from_shutterstock_page.click_previous_page()
            time.sleep(DELAY_TIME)
            current_page_amount = download_from_shutterstock_page.get_page_amount()
            case.result = False if not current_page_amount == 2 else True

            download_from_shutterstock_page.page_number.set_value('1')

        with uuid('904cd589-c1d4-4298-8560-de127cc7b553') as case:
            # 2.2. After Search
            # 2.2.2. Page number > Total Page number
            # show total page number
            # 21.1.4802: total page function = 3 if search keyword: pink ball play
            total_page_amount = download_from_shutterstock_page.get_total_page_amount()
            logger(total_page_amount)
            case.result = False if total_page_amount < 2 else True
        with uuid('29b33119-a6d0-4961-912e-838ce31c844d') as case:
            # 2.2. After Search
            # 2.2.3. Library Panel > Icons size / Thumbnail size > [ Extra Large Icons ]
            # Thumbnails show as extra large icons
            download_from_shutterstock_page.set_library_setting(value='Extra Large')

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_2_3_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_2_3_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.79)

        with uuid('21f46d53-29e2-4a9a-817d-fd37938667b9') as case:
            # 1.6. Scroll bar
            # 1.6.2. Check scroll bar >Resize Icon then Check Scroll bar status
            # if thumbnail size > default size, it will enable scroll bar
            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_1_6_2_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_1_6_2_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.scroll_media, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview)

        with uuid('974ae389-a1b4-4ba8-9930-5676b4d56c7a') as case:
            # 2.2. After Search
            # 2.2.3. Library Panel > Icons size / Thumbnail size > [ Large Icons ]
            # Thumbnails show as large icons
            download_from_shutterstock_page.set_library_setting(value='Large')

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_2_3_2.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_2_3_2.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.7)

        with uuid('c7affb86-323a-4f13-b68f-4d0535c502f5') as case:
            # 2.2. After Search
            # 2.2.3. Library Panel > Icons size / Thumbnail size > [ Small Icons ]
            # Thumbnails show as small icons
            download_from_shutterstock_page.set_library_setting(value='Small')

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_2_3_3.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_2_3_3.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.7)

        with uuid('e9211539-b22a-4582-a781-d0952d049de6') as case:
            # 2.2. After Search
            # 2.2.3. Library Panel > Icons size / Thumbnail size > [ Medium Icons ]
            # Thumbnails show as medium icons
            download_from_shutterstock_page.set_library_setting(value='Medium')

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_2_3_4.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_2_3_4.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.7)

        with uuid('44a7dad6-609b-4c80-8d88-ecf5e908f57e') as case:
            # 2.2. After Search
            # 2.2.4. Select / Deselect > Single select > CheckBox
            # Can select/ deselect single file by ticking the checkbox
            download_from_shutterstock_page.video.select_clip(value=1)
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            check_result_1 = False if not selected_amount == 1 else True
            check_result_2 = download_from_shutterstock_page.video.get_clip_status(value=1)
            check_result_3 = download_from_shutterstock_page.is_enabled_download()

            download_from_shutterstock_page.video.unselect_clip(value=1)
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            check_result_4 = False if not selected_amount == 0 else True
            check_result_5 = not (download_from_shutterstock_page.video.get_clip_status(value=1))
            check_result_6 = not (download_from_shutterstock_page.is_enabled_download())

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4 and check_result_5 \
                and check_result_6

        with uuid('9bfbeb1b-05cb-4227-8972-c45e6eb3b298') as case:
            # 2.2. After Search
            # 2.2.4. Select / Deselect > Single select > thumbnail
            # Can select/ deselect single file by clicking the thumbnail (no "Play" button area)
            download_from_shutterstock_page.video.click_thumbnail(index=1)
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            check_result_1 = False if not selected_amount == 1 else True
            check_result_2 = download_from_shutterstock_page.video.get_clip_status(value=1)
            check_result_3 = download_from_shutterstock_page.is_enabled_download()
            download_from_shutterstock_page.video.click_thumbnail(index=1)
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            check_result_4 = False if not selected_amount == 0 else True
            check_result_5 = not (download_from_shutterstock_page.video.get_clip_status(value=1))
            check_result_6 = not (download_from_shutterstock_page.is_enabled_download())

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4 and check_result_5 \
                and check_result_6

        with uuid('c858a601-9261-4ff1-b7d4-5cb819502ab2') as case:
            # 2.2. After Search
            # 2.2.4. Select / Deselect > Multiple select > CheckBox
            # Can select/ deselect multiple files by ticking the checkbox
            download_from_shutterstock_page.video.select_clip(value=[0, 1, 2])
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            check_result_1 = False if not selected_amount == 3 else True
            check_result_2 = download_from_shutterstock_page.video.get_clip_status(value=2)
            check_result_3 = download_from_shutterstock_page.is_enabled_download()

            download_from_shutterstock_page.video.unselect_clip(value=[0, 1, 2])
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            check_result_4 = False if not selected_amount == 0 else True
            check_result_5 = not (download_from_shutterstock_page.video.get_clip_status(value=2))
            check_result_6 = not (download_from_shutterstock_page.is_enabled_download())

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4 and check_result_5 \
                and check_result_6

        with uuid('8c6186aa-af7a-46c9-b81f-d5822012b225') as case:
            # 2.2. After Search
            # 2.2.8. Selected clip(s)
            # Update the number of the selected clip normally
            case.result = check_result_1

        with uuid('d248cdbe-30d9-4032-ac4a-f150ef41e34d') as case:
            # 2.2. After Search
            # 2.2.4. Select / Deselect > Multiple select > thumbnail
            # Can select/ deselect multiple files by clicking the thumbnail (no "Play" button area)
            download_from_shutterstock_page.video.click_thumbnail(index=0)
            download_from_shutterstock_page.video.click_thumbnail(index=1)
            download_from_shutterstock_page.video.click_thumbnail(index=2)
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            check_result_1 = False if not selected_amount == 3 else True
            check_result_2 = download_from_shutterstock_page.video.get_clip_status(value=2)
            check_result_3 = download_from_shutterstock_page.is_enabled_download()
            download_from_shutterstock_page.video.click_thumbnail(index=0)
            download_from_shutterstock_page.video.click_thumbnail(index=1)
            download_from_shutterstock_page.video.click_thumbnail(index=2)
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            check_result_4 = False if not selected_amount == 0 else True
            check_result_5 = not (download_from_shutterstock_page.video.get_clip_status(value=2))
            check_result_6 = not (download_from_shutterstock_page.is_enabled_download())

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4 and check_result_5 \
                and check_result_6

        with uuid('543f35e2-e690-4d07-b47e-2eb4d05e0b8b') as case:
            # 2.2. After Search
            # 2.2.7. [ Download ] > Select file
            # Button is enabled
            case.result = check_result_3

        with uuid('97f4fb63-06dd-4720-99be-5b461c96e51d') as case:
            # 2.2. After Search
            # 2.2.5. Browser Preview > Click the play button > Safari
            # Pop up a window and preview normally in the browser after hover thumbnail and click [play] button
            # 20.7.4210: Support Embedded window to preview SS content
            download_from_shutterstock_page.video.hover_thumbnail(index=1)
            main_page.mouse.click()
            case.result = download_from_shutterstock_page.close_pop_up_preview_window()

        with uuid('65decfc8-c841-46ea-8f0d-676e9833f785') as case:
            # 2.2. After Search
            # 2.2.6. Thumbnail > Adjust window size
            # Show the suitable size and thumbnail numbers if adjust window size
            download_from_shutterstock_page.adjust_window(x=325, y=61, w=949, h=747)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_2_6_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_2_6_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.75)

        with uuid('d3719d6c-d0b0-411b-a895-6fa9549364d1') as case:
            # 2.2. After Search
            # 2.2.6. Thumbnail > Checkbox
            # Show checkbox normally in upper right corner
            download_from_shutterstock_page.video.hover_thumbnail(index=0)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_2_6_2.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_2_6_2.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_clip, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.75)

        with uuid('736375e5-b82b-46cc-9a52-35940d52f606') as case:
            # 2.2. After Search
            # 2.2.6. Thumbnail > Highlight
            # Show highlight thumbnail if tick checkbox
            download_from_shutterstock_page.video.select_clip(value=1)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_2_6_3.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_2_6_3.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_scroll_view, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.75)

        with uuid('343e53fa-4d85-49d5-a20c-1a5535e4b322') as case:
            # 2.2. After Search
            # 2.2.6. Thumbnail > Tooltip > hover
            # Show detail profile information
            case.result = download_from_shutterstock_page.video.verify_thumbnail_tooltip(
                Ground_Truth_Folder + 'shutterstock_2_2_6_4.png', index=0)

        with uuid('8c237ea6-3d6b-4959-9768-2723265ffa51') as case:
            # 2.2. After Search
            # 2.2.7. [ Download ] > Progress bar/ Percent
            # Show "Downloading Files[#%]"/ "Remaining Time:" normally
            download_from_shutterstock_page.video.select_clip(value=0)
            time.sleep(DELAY_TIME*0.5)
            download_from_shutterstock_page.click_download()
            case.result = download_from_shutterstock_page.download.verify_progress()

        with uuid('f977e973-85c8-4054-9c46-f90c0e62eb6a') as case:
            # 2.2. After Search
            # 2.2.7. [ Download ] > [ Cancel ]
            # Cancel downloading
            check_result_1 = download_from_shutterstock_page.download.click_cancel()
            time.sleep(DELAY_TIME*2)
            logger(check_result_1)
            check_result_2 = not (download_from_shutterstock_page.download.has_dialog())
            logger(check_result_2)
            case.result = check_result_1 and check_result_2
        with uuid('6c986e67-2728-40d7-a4f6-76be423b097d') as case:
            # 2.2. After Search
            # 2.2.7. [ Download ] > Complete > Dialog
            # Pop up a dialog "The clips are successfully downloaded and…"
            download_from_shutterstock_page.click_download()

            download_from_shutterstock_page.find(L.download_from_shutterstock.download.hd_video.btn_no, timeout=250)
            download_from_shutterstock_page.download.hd_video.click_no()
            time.sleep(DELAY_TIME)
            download_from_shutterstock_page.download.hd_video.click_no()
            x = 0
            for x in range(30):
                if x == 29:
                    case.result = False
                    logger('time out')
                if download_from_shutterstock_page.exist(L.download_from_shutterstock.download.txt_complete_msg).AXValue.startswith('The clips were successfully'):
                    case.result = True
                    logger(x)
                    break
                time.sleep(DELAY_TIME)

            download_from_shutterstock_page.download.click_complete_ok()
            time.sleep(DELAY_TIME * 15)
            download_from_shutterstock_page.click_close()
            time.sleep(DELAY_TIME)

        with uuid('0cced0e3-e365-4fe9-b661-0dfef4813607') as case:
            # 2.2. After Search
            # 2.2.7. [ Download ] > Complete
            # Downloaded clips are available in the media library
            case.result = media_room_page.select_media_content('22134577_01_fhd')

            # Delete the download clips from SS
            main_page.select_library_icon_view_media('22134577_01_fhd')
            main_page.right_click()
            main_page.select_right_click_menu('Remove from Disk')
            main_page.exist_click(L.media_room.confirm_dialog.btn_yes, timeout=5)

            time.sleep(DELAY_TIME)
            main_page.select_library_icon_view_media('1016118532_01_fhd')
            main_page.right_click()
            main_page.select_right_click_menu('Remove from Disk')
            main_page.exist_click(L.media_room.confirm_dialog.btn_yes, timeout=5)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid('7c5eaf84-e6c7-42f6-be7e-855188b3a236') as case:
            # 2.3. Popular Keyword Search
            # 2.3.1. Animation
            # check the search result whether is matched keyword or not
            media_room_page.import_media_from_shutterstock()
            time.sleep(4)
            gettyimage_page.switch_to_SS()
            time.sleep(4)
            # waiting for shutterstock enable
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=10)

            download_from_shutterstock_page.search.search_text('animation')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_3_1_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_3_1_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_scroll_view, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.8)

        with uuid('cf15643a-d577-42fc-8b82-12f6efee5ce8') as case:
            # 2.3. Popular Keyword Search
            # 2.3.2. Business
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('business')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_3_2_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_3_2_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_scroll_view, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.8)

        with uuid('0e8a7e1c-60b8-4643-880d-df30c14a02c2') as case:
            # 2.3. Popular Keyword Search
            # 2.3.3. Nature
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('nature')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_3_3_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_3_3_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_scroll_view, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.70)

        with uuid('ca8c650a-0686-4195-896b-86a3d807aa17') as case:
            # 2.3. Popular Keyword Search
            # 2.3.4. Technology
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('technology')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_3_4_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_3_4_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_scroll_view, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.70)

        with uuid('7c62a729-1d23-4d36-a1ed-27ae558995da') as case:
            # 2.3. Popular Keyword Search
            # 2.3.5. People
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('people')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_3_5_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_3_5_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_scroll_view, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.6)

        with uuid('0978017f-9750-43e0-ae37-943d08700556') as case:
            # 2.3. Popular Keyword Search
            # 2.3.6. Slow Motion
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('slow motion')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_3_6_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_3_6_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_scroll_view, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.7)

        with uuid('01cc7f37-eee7-47b5-9000-33199da9d83f') as case:
            # 2.3. Popular Keyword Search
            # 2.3.7. Football
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('football')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_3_7_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_3_7_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_scroll_view, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.70)

        with uuid('e5a18d49-1acb-45f7-88c8-e7b960caf8e7') as case:
            # 2.3. Popular Keyword Search
            # 2.3.8. Beach
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('beach')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_3_8_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_3_8_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_scroll_view, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview)

        with uuid('9cd04a73-d2b8-4c87-b683-3b072a339459') as case:
            # 2.3. Popular Keyword Search
            # 2.3.9. Funny
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('funny')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_3_9_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_3_9_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_scroll_view, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.70)

        with uuid('7530bc4e-f9f2-42ef-b636-6a03272ca746') as case:
            # 2.3. Popular Keyword Search
            # 2.3.10. Food
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('food')
            time.sleep(DELAY_TIME * 10)
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_2_3_10_1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_2_3_10_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_scroll_view, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.8)

# ======================================================================================================================
# M3 Test Case

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid('8c31ef1c-8a8b-4b3e-8f8e-2b6c76c86773') as case:
            # 3. Photo
            # 3.1. Before Search
            # 3.1.1. Search box > Default text
            # Show "Search"/ Empty in the search box
            media_room_page.import_media_from_shutterstock()
            time.sleep(4)
            gettyimage_page.switch_to_SS()
            time.sleep(4)
            # waiting for shutterstock ready
            download_from_shutterstock_page.is_exist(L.download_from_shutterstock.frame_clips, timeout=10)
            time.sleep(1)
            download_from_shutterstock_page.switch_to_photo()
            time.sleep(1)
            case.result = download_from_shutterstock_page.search.verify_default_string(default='Search')

            time.sleep(DELAY_TIME * 8)

        with uuid('5aef1757-e5ca-4ce9-a544-4775317967cb') as case:
            # 3.1. Before Search
            # 3.1.1. Search box > Tooltip
            # Show "Search"
            case.result = download_from_shutterstock_page.search.verify_tooltip(
                Ground_Truth_Folder + 'shutterstock_3_1_1-1.png')

        with uuid('2f50ea97-2d4e-4f69-b5a5-396524189839') as case:
            # 3.1. Before Search
            # 3.1.2. Library Panel > Default icons size > [Medium icons]
            # Thumbnails show as Medium icons. One page has 30 icons
            # 20.7.4210 : Only 12 in current preview area (no scroll down)
            current_setting = download_from_shutterstock_page.get_library_setting()
            check_result_1 = False if not current_setting == 'Medium' else True

            download_from_shutterstock_page.photo.hover_thumbnail(index=0)  # hover on first clip
            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            logger(clip_number)
            check_result_2 = False if not clip_number == 12 else True

            case.result = check_result_1 and check_result_2

        with uuid('8f55820d-d811-4668-93ab-158f549307c4') as case:
            # 3.1. Before Search
            # 3.1.3. Page number > Current Page number
            # Default value is "1"
            current_page_amount = download_from_shutterstock_page.get_page_amount()
            case.result = False if not current_page_amount == 1 else True

        with uuid('eadbb29a-f808-44c3-8524-5d8cd893b19b') as case:
            # 3.1. Before Search
            # 3.1.3. Page number > Total Page number
            # Total Page number
            total_page_amount = download_from_shutterstock_page.get_total_page_amount()
            logger(total_page_amount)
            case.result = False if total_page_amount < 15 else True

        with uuid('784ed18a-c786-4005-b462-6573c79ce5c9') as case:
            # 3.1. Before Search
            # 3.1.4. [Download] > Default status
            # Button is disabled
            button_status = download_from_shutterstock_page.is_enabled_download()
            case.result = True if not button_status else False

        with uuid('9bfa0180-cafe-4d33-bb3c-72b2a021f73a') as case:
            # 3.1. Before Search
            # 3.1.4. [Download] > Tooltip
            # Show "Download"
            case.result = download_from_shutterstock_page.verify_download_tooltip(
                Ground_Truth_Folder + 'shutterstock_3_1_4-1.png')

        with uuid('c7f553d0-fd5a-45da-b958-64871629baa5') as case:
            # 3.1. Before Search
            # 3.1.5. Selected clip(s) > Default value
            # Show "0 clips"
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            case.result = False if not selected_amount == 0 else True

        with uuid('8c0a24ef-9d25-4fad-a3e9-893b1e8ffad8') as case:
            # 3.2. After Search
            # 3.2.1. Search box > Input keyword
            # Show the string which is user keyin
            download_from_shutterstock_page.search.search_text('airport')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'airport' else True

            time.sleep(DELAY_TIME * 8)

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result_2 = False if not clip_number == 12 else True

            case.result = check_result_1 and check_result_2

        with uuid('c102af90-3380-4a6c-989b-6afd8cf0ea98') as case:
            # 3.2. After Search
            # 3.2.2. Page number > Input page number > input box
            # check current page and library panel is updated to user keyin number
            download_from_shutterstock_page.page_number.set_value('3')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=10)

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result = False if not clip_number == 12 else True
            case.result = check_result

        with uuid('f07479e0-7670-4035-8aa0-5e625a17df94') as case:
            # 3.2. After Search
            # 3.2.2. Page number > Current Page number
            # update current page if click [next/previous] page
            for press_times in range(2):
                download_from_shutterstock_page.click_next_page()
                time.sleep(DELAY_TIME)
            download_from_shutterstock_page.click_previous_page()
            time.sleep(DELAY_TIME)
            current_page_amount = download_from_shutterstock_page.get_page_amount()
            case.result = False if not current_page_amount == 4 else True

            download_from_shutterstock_page.page_number.set_value('1')

        with uuid('ed115af3-99d8-4278-b5c8-0e287f8f3ca6') as case:
            # 3.2. After Search
            # 3.2.2. Page number > Total Page number
            # show total page number
            total_page_amount = download_from_shutterstock_page.get_total_page_amount()
            case.result = False if total_page_amount < 31 else True

        with uuid('3db4ff82-ac34-473e-b0c7-421a0f4e7856') as case:
            # 3.2. After Search
            # 3.2.3. Library Panel > Icons size / Thumbnail size > [ Extra Large Icons ]

            # Clear search
            download_from_shutterstock_page.search.click_clear()
            time.sleep(DELAY_TIME * 2)
            # Search other keyword "airport five man"
            download_from_shutterstock_page.search.search_text('airport five man')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)
            # Thumbnails show as extra large icons
            download_from_shutterstock_page.set_library_setting(value='Extra Large')

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result = False if clip_number != 4 else True
            logger(clip_number)
            case.result = check_result

        with uuid('7074b801-8e03-4b57-bcc7-27ea6cb65b7f') as case:
            # 3.2. After Search
            # 3.2.3. Library Panel > Icons size / Thumbnail size > [ Large Icons ]
            # Thumbnails show as large icons
            download_from_shutterstock_page.set_library_setting(value='Large')

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result = False if not clip_number == 6 else True
            case.result = check_result

        with uuid('7d23b802-685f-4058-bbfe-0dd0c319f34e') as case:
            # 3.2. After Search
            # 3.2.3. Library Panel > Icons size / Thumbnail size > [ Small Icons ]
            # Thumbnails show as small icons
            download_from_shutterstock_page.set_library_setting(value='Small')

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            logger(clip_number)
            check_result = False if clip_number < 25 else True
            case.result = check_result

        with uuid('ca455136-73fb-4d7f-9a2b-c8505244607b') as case:
            # 3.2. After Search
            # 3.2.3. Library Panel > Icons size / Thumbnail size > [ Medium Icons ]
            # Thumbnails show as medium icons
            download_from_shutterstock_page.set_library_setting(value='Medium')

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result = False if not clip_number == 12 else True
            case.result = check_result

        with uuid('b885ac3d-e27c-4c64-b155-4f429251d724') as case:
            # 3.2. After Search
            # 3.2.4. Select / Deselect > Single select > CheckBox
            # Can select/ deselect single file by ticking the checkbox
            download_from_shutterstock_page.photo.select_clip(value=1)
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            check_result_1 = False if not selected_amount == 1 else True
            check_result_2 = download_from_shutterstock_page.photo.get_clip_status(index=1)
            check_result_3 = download_from_shutterstock_page.is_enabled_download()

            download_from_shutterstock_page.photo.unselect_clip(value=1)
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            check_result_4 = False if not selected_amount == 0 else True
            check_result_5 = not (download_from_shutterstock_page.photo.get_clip_status(index=1))
            check_result_6 = not (download_from_shutterstock_page.is_enabled_download())

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4 and check_result_5 \
                and check_result_6

        with uuid('cc248b95-41ec-4bf8-8ca0-c7f3a76a919c') as case:
            # 3.2. After Search
            # 3.2.4. Select / Deselect > Single select > thumbnail
            # Can select/ deselect single file by clicking the thumbnail (no "Play" button area)
            download_from_shutterstock_page.photo.click_thumbnail(value=1)
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            check_result_1 = False if not selected_amount == 1 else True
            check_result_2 = download_from_shutterstock_page.photo.get_clip_status(index=1)
            check_result_3 = download_from_shutterstock_page.is_enabled_download()
            download_from_shutterstock_page.photo.click_thumbnail(value=1)
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            check_result_4 = False if not selected_amount == 0 else True
            check_result_5 = not (download_from_shutterstock_page.photo.get_clip_status(index=1))
            check_result_6 = not (download_from_shutterstock_page.is_enabled_download())

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4 and check_result_5 \
                and check_result_6

        with uuid('a40ed246-4b95-4c52-bcae-30cfa9078c67') as case:
            # 3.2. After Search
            # 3.2.4. Select / Deselect > Multiple select > CheckBox
            # Can select/ deselect multiple files by ticking the checkbox
            download_from_shutterstock_page.photo.select_clip(value=0)
            download_from_shutterstock_page.photo.select_clip(value=1)
            download_from_shutterstock_page.photo.select_clip(value=2)
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            check_result_1 = False if not selected_amount == 3 else True
            check_result_2 = download_from_shutterstock_page.photo.get_clip_status(index=2)
            check_result_3 = download_from_shutterstock_page.is_enabled_download()

            download_from_shutterstock_page.photo.unselect_clip(value=0)
            download_from_shutterstock_page.photo.unselect_clip(value=1)
            download_from_shutterstock_page.photo.unselect_clip(value=2)
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            check_result_4 = False if not selected_amount == 0 else True
            check_result_5 = not (download_from_shutterstock_page.photo.get_clip_status(index=2))
            check_result_6 = not (download_from_shutterstock_page.is_enabled_download())

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4 and check_result_5 \
                and check_result_6

        with uuid('44746f3d-15cb-4da9-972c-6230489dd135') as case:
            # 3.2. After Search
            # 3.2.8. Selected clip(s)
            # Update the number of the selected clip normally
            case.result = check_result_1

        with uuid('48b68fd6-56d4-44c0-9bba-683bf1941927') as case:
            # 3.2. After Search
            # 3.2.4. Select / Deselect > Multiple select > thumbnail
            # Can select/ deselect multiple files by clicking the thumbnail (no "Play" button area)
            download_from_shutterstock_page.photo.click_thumbnail(value=0)
            download_from_shutterstock_page.photo.click_thumbnail(value=1)
            download_from_shutterstock_page.photo.click_thumbnail(value=2)
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            check_result_1 = False if not selected_amount == 3 else True
            check_result_2 = download_from_shutterstock_page.photo.get_clip_status(index=2)
            check_result_3 = download_from_shutterstock_page.is_enabled_download()
            download_from_shutterstock_page.photo.click_thumbnail(value=0)
            download_from_shutterstock_page.photo.click_thumbnail(value=1)
            download_from_shutterstock_page.photo.click_thumbnail(value=2)
            time.sleep(DELAY_TIME)
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            time.sleep(DELAY_TIME)
            check_result_4 = False if not selected_amount == 0 else True
            check_result_5 = not (download_from_shutterstock_page.photo.get_clip_status(index=2))
            check_result_6 = not (download_from_shutterstock_page.is_enabled_download())
            logger(check_result_1)
            logger(check_result_2)
            logger(check_result_3)
            logger(check_result_4)
            logger(check_result_5)
            logger(check_result_6)
            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4 and check_result_5 \
                and check_result_6

        with uuid('8a14bdb5-5309-4c03-a31a-82d5638834af') as case:
            # 3.2. After Search
            # 3.2.7. [ Download ] > Select file
            # Button is enabled
            case.result = check_result_3

        with uuid('954df3f9-9f7c-4fb5-ae97-6860ebffe7b9') as case:
            # 3.2. After Search
            # 3.2.5. Preview > Click the play button > Safari
            # Pop up a window and preview normally in the browser after hover thumbnail and click [play] button
            download_from_shutterstock_page.video.hover_thumbnail(index=0)
            main_page.mouse.click()
            case.result = download_from_shutterstock_page.close_pop_up_preview_window()

        with uuid('e97adb6b-76f2-4c48-b87d-d81a7ed79cef') as case:
            # 3.2. After Search
            # 3.2.6. Thumbnail > Checkbox
            # Show checkbox normally in upper right corner
            download_from_shutterstock_page.photo.hover_thumbnail(index=0)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_3_2_6-2.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_3_2_6-2.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_clip, file_name=image_full_path)
            check_snapshot_result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.9)
            case.result = check_snapshot_result

        with uuid('ca4c1830-7148-435c-bb96-9959ae9ecedf') as case:
            # 3.2. After Search
            # 3.2.6. Thumbnail > Tooltip > hover
            # Show detail profile information

            # 20.7.4228 : Due to tooltip position does NOT keep its positon, so only check GT result
            # ORG case detail:
            # case.result = download_from_shutterstock_page.photo.verify_thumbnail_tooltip(
            #     Ground_Truth_Folder + 'shutterstock_3_2_6-4.png', index=0)

            case.result = check_snapshot_result

        with uuid('ec960f27-d41f-4d60-96a6-2bc78d05f17b') as case:
            # 3.2. After Search
            # 3.2.6. Thumbnail > Highlight
            # Show highlight thumbnail if tick checkbox
            main_page.move_mouse_to_0_0()
            time.sleep(2)
            download_from_shutterstock_page.photo.select_clip(value=0)
            download_from_shutterstock_page.photo.select_clip(value=1)
            download_from_shutterstock_page.photo.select_clip(value=2)
            download_from_shutterstock_page.photo.select_clip(value=3)
            download_from_shutterstock_page.photo.select_clip(value=4)
            download_from_shutterstock_page.photo.select_clip(value=5)
            download_from_shutterstock_page.photo.select_clip(value=6)
            download_from_shutterstock_page.photo.select_clip(value=7)
            download_from_shutterstock_page.photo.select_clip(value=8)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_3_2_6-3.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_3_2_6-3.png'
            current_selected = {"AXIdentifier": "ShutterstockCollectionViewItem", 'index': 8}
            current_preview = download_from_shutterstock_page.snapshot(
                locator=current_selected, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview)

        with uuid('dcf39c3a-246f-4338-982d-cc33eaefd5f8') as case:
            # 3.2. After Search
            # 3.2.6. Thumbnail > Adjust window size
            # Show the suitable size and thumbnail numbers if adjust window size
            download_from_shutterstock_page.adjust_window(x=325, y=61, w=949, h=747)
            time.sleep(DELAY_TIME)

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            logger(clip_number)
            check_result = False if clip_number <= 15 else True
            case.result = check_result

        with uuid('145a274e-dc35-4c3c-9d8b-cbd20de1b5a4') as case:
            # 3.2. After Search
            # 3.2.7. [ Download ] > Progress bar/ Percent
            # Show "Downloading Files[#%]"/ "Remaining Time:" normally
            download_from_shutterstock_page.click_download()
            case.result = download_from_shutterstock_page.download.verify_progress()

        with uuid('b3bf2959-8e63-45f3-826b-4321f9c45638') as case:
            # 3.2. After Search
            # 3.2.7. [ Download ] > [ Cancel ]
            # Cancel downloading
            check_result_1 = download_from_shutterstock_page.download.click_cancel()
            time.sleep(DELAY_TIME)
            check_result_2 = not (download_from_shutterstock_page.download.has_dialog())

            case.result = check_result_1 and check_result_2

        with uuid('68361681-7d73-4934-a9b3-3918be36aa67') as case:
            # 3.2. After Search
            # 3.2.7. [ Download ] > Complete > Dialog
            # Pop up a dialog "The clips are successfully downloaded and…"

            # un-tick 8 files / only download 1st thumbnail
            download_from_shutterstock_page.photo.click_thumbnail(value=1)
            download_from_shutterstock_page.photo.click_thumbnail(value=2)
            download_from_shutterstock_page.photo.click_thumbnail(value=3)
            download_from_shutterstock_page.photo.click_thumbnail(value=4)
            download_from_shutterstock_page.photo.click_thumbnail(value=5)
            download_from_shutterstock_page.photo.click_thumbnail(value=6)
            download_from_shutterstock_page.photo.click_thumbnail(value=7)
            download_from_shutterstock_page.photo.click_thumbnail(value=8)

            download_from_shutterstock_page.click_download()

            case.result = download_from_shutterstock_page.is_exist(
                {'AXIdentifier': 'IDD_CLALERT', 'AXRoleDescription': 'dialog'}, timeout=15)

            download_from_shutterstock_page.download.click_complete_ok()
            time.sleep(DELAY_TIME * 15)
            download_from_shutterstock_page.click_close()
            time.sleep(DELAY_TIME)

        with uuid('cc4013bb-5ee6-44cd-9882-836a0f05ac33') as case:
            # 3.2. After Search
            # 3.2.7. [ Download ] > Complete
            # Downloaded clips are available in the media library
            # 20.6:1210000891_01
            # 20.7.4210: 26170943_01_fhd
            case.result = media_room_page.select_media_content('216109993_01')

            # remove downloaded content
            time.sleep(DELAY_TIME*2)
            media_room_page.hover_library_media('216109993_01')
            media_room_page.right_click()
            media_room_page.select_right_click_menu('Remove from Disk')
            media_room_page.exist_click(L.media_room.confirm_dialog.btn_yes)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid('a0d28e21-3946-4ff0-aa88-55d9c1f1daa8') as case:
            # 3.3. Popular Keyword Search
            # 3.3.1. Animals
            # check the search result whether is matched keyword or not
            media_room_page.import_media_from_shutterstock()
            time.sleep(4)
            gettyimage_page.switch_to_SS()
            time.sleep(4)
            # waiting for shutterstock enable
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=10)
            download_from_shutterstock_page.switch_to_photo()

            download_from_shutterstock_page.search.search_text('animals')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result = False if not clip_number > 5 else True
            case.result = check_result

        with uuid('2618201d-1550-4c09-a019-e964fe9420d2') as case:
            # 3.3. Popular Keyword Search
            # 3.3.2. Background
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('background')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result = False if not clip_number > 5 else True
            case.result = check_result

        with uuid('d6e8a698-5ee6-41c2-a4a3-d180e615b250') as case:
            # 3.3. Popular Keyword Search
            # 3.3.3. Fashion
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('fashion')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result = False if not clip_number > 5 else True
            case.result = check_result

        with uuid('0f260aa5-d16d-498c-a5a9-c0a3dcf9707d') as case:
            # 3.3. Popular Keyword Search
            # 3.3.4. local landmark
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('local landmark')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result = False if not clip_number > 5 else True
            case.result = check_result

        with uuid('5c87dbe2-e33b-460d-b11e-be2c61169483') as case:
            # 3.3. Popular Keyword Search
            # 3.3.5. Food
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('food')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result = False if not clip_number > 5 else True
            case.result = check_result

        with uuid('2cd4cbe2-8543-4b58-bac5-31c9710592ff') as case:
            # 3.3. Popular Keyword Search
            # 3.3.6. Holidays
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('holidays')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result = False if not clip_number > 5 else True
            case.result = check_result

        with uuid('55bb8721-6138-4c66-844a-ca91915ea659') as case:
            # 3.3. Popular Keyword Search
            # 3.3.7. Nature
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('nature')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result = False if not clip_number > 5 else True
            case.result = check_result

        with uuid('ffe88362-433f-48bf-9f6b-04400054ae08') as case:
            # 3.3. Popular Keyword Search
            # 3.3.8. People
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('people')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result = False if not clip_number > 5 else True
            case.result = check_result

        with uuid('97dba36f-fe02-43a6-96ba-a257891da97f') as case:
            # 3.3. Popular Keyword Search
            # 3.3.9. Sports
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('sports')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result = False if not clip_number > 5 else True
            case.result = check_result

        with uuid('e472b10b-70e2-4e7c-a8d3-09614a193943') as case:
            # 3.3. Popular Keyword Search
            # 3.3.10. Transportation
            # check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('transportation')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            clip_number = len(
                download_from_shutterstock_page.exist(L.download_from_shutterstock.frame_section).AXChildren)
            check_result = False if not clip_number > 5 else True
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid('f37f0cf2-0aee-478c-8ea0-a6c5fd27ed7f') as case:
            # 4. Music
            # 4.1. Before Search
            # 4.1.1. Search box > Default text
            # show "search"/ empty in the search box
            media_room_page.import_media_from_shutterstock()
            time.sleep(4)
            gettyimage_page.switch_to_SS()
            time.sleep(4)
            # waiting for shutterstock ready
            download_from_shutterstock_page.is_exist(L.download_from_shutterstock.frame_clips, timeout=10)
            download_from_shutterstock_page.switch_to_music()
            case.result = download_from_shutterstock_page.search.verify_default_string(default='Search')

            time.sleep(DELAY_TIME * 8)

        with uuid('28452827-9214-41f3-aead-cb56fc0e12cc') as case:
            # 4.1. Before Search
            # 4.1.1. Search box > Tooltip
            # show "search"
            check_result = download_from_shutterstock_page.search.verify_tooltip(
                Ground_Truth_Folder + 'shutterstock_4_1_1-1.png')
            case.result = check_result

        with uuid('81d3848e-9566-410f-8590-756783b9295d') as case:
            # 4.1. Before Search
            # 4.1.2. Preview > Play Button
            # button is disabled
            case.result = not(download_from_shutterstock_page.music.get_play_status())

        with uuid('faf4a4f8-2da2-43d4-b0f4-bf7420f2d6cb') as case:
            # 4.1. Before Search
            # 4.1.2. Preview > Pause Button
            # button is disabled
            download_from_shutterstock_page.music.click_play()
            case.result = not(download_from_shutterstock_page.music.get_play_status())

        with uuid('55c6d547-eea0-42e8-8a92-75f58da09a9a') as case:
            # 4.1. Before Search
            # 4.1.2. Preview > Stop Button
            # button is disabled
            case.result = not(download_from_shutterstock_page.music.get_stop_status())

        with uuid('f47f011d-45fb-4738-a3a1-4e6e5af46112') as case:
            # 4.1. Before Search
            # 4.1.2. Preview > Hotkey
            # able to use hotkey control preview
            media_room_page.press_space_key()
            time.sleep(DELAY_TIME * 3)
            case.result = not(download_from_shutterstock_page.music.get_play_status())

        with uuid('ba27139c-406c-4c31-97b3-dc637edbdbeb') as case:
            # 4.1. Before Search
            # 4.1.3. Volume > Adjust volume size
            # button is disabled > should enable
            case.result = download_from_shutterstock_page.find(
                L.download_from_shutterstock.music.btn_volumn).AXEnabled

        with uuid('9ee86282-2467-4b20-bf25-8bb937d66d67') as case:
            # 4.1. Before Search
            # 4.1.3. Volume > Mute
            # button is disabled > should enable
            case.result = download_from_shutterstock_page.find(
                L.download_from_shutterstock.music.btn_mute).AXEnabled

        with uuid('4353f341-d080-4f0e-9646-8b85e7ed013c') as case:
            # 4.1. Before Search
            # 4.1.4. List Panel > Increasing / Decreasing
            # select sort feature by click name/artist/genre/length/tempo item (not using [sort by] drop down menu)
            check_result_1 = download_from_shutterstock_page.music.is_ascending(index=0)
            check_available_music = download_from_shutterstock_page.music.check_music_icon_number()
            logger(check_available_music)
            check_result_2 = False if not check_available_music >= 1000 else True

            case.result = check_result_1 and check_result_2

        with uuid('148b85e2-fb3e-4c65-a8b5-3ad3068db8fd') as case:
            # 4.1. Before Search
            # 4.1.4. List Panel > Library menu > [Sort by] > Default
            # sort by 'Name'
            current_setting = download_from_shutterstock_page.music.get_sort_by()
            case.result = False if not current_setting == 'Name' else True

        with uuid('d40d9557-bd4c-47f5-9135-784c203a6f8c') as case:
            # 4.1. Before Search
            # 4.1.4. List Panel > Library menu > [Sort by] > [Artist]
            # can be sorted by artist normally
            download_from_shutterstock_page.music.set_sort_by(1)  # sort by artist
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_4_1_4-3.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_4_1_4-3.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.music.menu_table_header_view, file_name=image_full_path)
            check_result = download_from_shutterstock_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('08d4a54c-19a9-4e1b-aed1-f28129e6caac') as case:
            # 4.1. Before Search
            # 4.1.4. List Panel > Library menu > [Sort by] > [Length]
            # can be sorted by length normally
            download_from_shutterstock_page.music.set_sort_by(2)  # sort by length
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_4_1_4-4.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_4_1_4-4.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.music.menu_table_header_view, file_name=image_full_path)
            check_result = download_from_shutterstock_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('968333c0-d357-4be2-ab21-d1e819f518dd') as case:
            # 4.1. Before Search
            # 4.1.4. List Panel > Library menu > [Sort by] > [BPM(Tempo)]
            # can be sorted by tempo normally
            download_from_shutterstock_page.music.set_sort_by(3)  # sort by BPM(tempo)
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_4_1_4-5.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_4_1_4-5.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.music.menu_table_header_view, file_name=image_full_path)
            check_result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.75)
            case.result = check_result

        with uuid('79beb791-3fc4-4fb0-8a5a-2ccccf88d52a') as case:
            # 4.1. Before Search
            # 4.1.4. List Panel > Library menu > [Sort by] > [Name]
            # can be sorted by name normally
            download_from_shutterstock_page.music.set_sort_by(0)  # sort by name
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_4_1_4-6.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_4_1_4-6.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.music.menu_table_header_view, file_name=image_full_path)
            check_result = download_from_shutterstock_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('96f6ab50-e94d-408c-9833-78004855051c') as case:
            # 4.1. Before Search
            # 4.1.5. [Download] > Default status
            # button is disabled
            button_status = download_from_shutterstock_page.is_enabled_download()
            case.result = True if not button_status else False

        with uuid('249bbe4b-a4f5-4b46-8529-85423e428292') as case:
            # 4.1. Before Search
            # 4.1.5. [Download] > Tooltip
            # show 'Download'
            case.result = download_from_shutterstock_page.verify_download_tooltip(
                Ground_Truth_Folder + 'shutterstock_4_1_5-1.png')

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        with uuid('b8133599-f5a0-406c-88dc-d966d3c5fbbc') as case:
            # 4.2. After Search
            # 4.2.1. Search box > input keyword
            # Show the string which is user keyin
            time.sleep(2)
            media_room_page.import_media_from_shutterstock()
            time.sleep(10)
            gettyimage_page.switch_to_SS()
            time.sleep(4)
            download_from_shutterstock_page.is_exist(L.download_from_shutterstock.frame_clips, timeout=10)
            download_from_shutterstock_page.switch_to_music()
            download_from_shutterstock_page.find(L.download_from_shutterstock.music.table_clip, timeout=10)
            download_from_shutterstock_page.search.search_text('good evening')
            download_from_shutterstock_page.find(L.download_from_shutterstock.music.table_clip, timeout=10)

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'good evening' else True

            time.sleep(DELAY_TIME * 5)

            check_available_music = download_from_shutterstock_page.music.check_music_icon_number()
            check_result_2 = False if not check_available_music > 3 else True

            case.result = check_result_1 and check_result_2

        with uuid('82018f20-06ff-4145-8ca4-d11a5cee8cec') as case:
            # 4.2. After Search
            # 4.2.2. Preview > Play Button
            # Can Preview normally
            download_from_shutterstock_page.music.select_song('Cozy Evening')
            # wait play button ready
            for x in range(10):
                if download_from_shutterstock_page.music.get_play_status():
                    check_result = download_from_shutterstock_page.exist_press(
                        L.download_from_shutterstock.music.btn_play)
                    # check_result = download_from_shutterstock_page.music.click_play()
                    logger('break')
                    break
                if x == 9:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)
            case.result = check_result

            time.sleep(DELAY_TIME * 5)

        with uuid('17ed28b0-bb85-47be-b904-660e98fa9101') as case:
            # 4.2. After Search
            # 4.2.2. Preview > Pause Button
            # Can pause music
            check_result = download_from_shutterstock_page.exist_press(L.download_from_shutterstock.music.btn_pause)
            # check_result = download_from_shutterstock_page.music.click_pause()
            case.result = check_result

        with uuid('5ab4785b-d520-484c-8d0a-28190fa7986e') as case:
            # 4.2. After Search
            # 4.2.2. Preview > Play one music(A) and click other music (B)
            # Can stop music (A) and preview music (B) normally > should no preview music B
            download_from_shutterstock_page.music.click_play()
            time.sleep(DELAY_TIME * 5)
            download_from_shutterstock_page.music.select_song('Evening Hip-Hop')
            case.result = download_from_shutterstock_page.music.get_play_status()

        with uuid('b40991dd-e6f8-4c50-a19c-732a77944da6') as case:
            # 4.2. After Search
            # 4.2.2. Preview > Play one music and Change other tab (Video / Photo)
            # Can stop music and Go to other tab (Video / Photo)
            download_from_shutterstock_page.exist_press(L.download_from_shutterstock.music.btn_play)
            # download_from_shutterstock_page.music.click_play()
            time.sleep(DELAY_TIME * 5)
            download_from_shutterstock_page.switch_to_video()
            time.sleep(DELAY_TIME * 2)
            check_result_1 = download_from_shutterstock_page.is_exist(L.download_from_shutterstock.frame_clips, timeout=10)
            time.sleep(DELAY_TIME * 5)

            download_from_shutterstock_page.switch_to_music()
            time.sleep(DELAY_TIME * 5)
            #download_from_shutterstock_page.find(L.download_from_shutterstock.music.frame_scroll_view, timeout=10)
            download_from_shutterstock_page.music.select_song('Even Flow')
            time.sleep(DELAY_TIME * 5)
            check_result_2 = download_from_shutterstock_page.music.get_play_status()
            logger(check_result_1)
            logger(check_result_2)
            case.result = check_result_1 and check_result_2

        with uuid('fcb4c51e-367a-4519-9f1c-248f0c84e8ae') as case:
            # 4.2. After Search
            # 4.2.3. Volume > Adjust volume size
            # Adjust the volume size to check audio volume
            download_from_shutterstock_page.music.select_song('Cozy Evening')
            # wait play button ready
            for x in range(10):
                if download_from_shutterstock_page.music.get_play_status():
                    download_from_shutterstock_page.exist_press(L.download_from_shutterstock.music.btn_play)
                    # download_from_shutterstock_page.music.click_play()
                    logger('break')
                    break
                if x == 9:
                    logger('Tab cannot active [Time out]')
                    raise Exception
                time.sleep(DELAY_TIME)

            check_result_1 = download_from_shutterstock_page.music.adjust_volume(0.5)
            time.sleep(DELAY_TIME * 5)

            check_available_music = download_from_shutterstock_page.music.check_music_icon_number()
            check_result_2 = False if not check_available_music > 3 else True

            case.result = check_result_1 and check_result_2

        with uuid('53a96a51-b3bd-4f0f-a793-bb2519bed0f2') as case:
            # 4.2. After Search
            # 4.2.3. Volume > Mute
            # Can mute
            check_result_1 = download_from_shutterstock_page.music.click_mute()
            time.sleep(DELAY_TIME)
            check_available_music = download_from_shutterstock_page.music.check_music_icon_number()
            check_result_2 = False if not check_available_music > 3 else True

            case.result = check_result_1 and check_result_2

            download_from_shutterstock_page.music.click_mute()
            download_from_shutterstock_page.music.adjust_volume(1.0)

        with uuid('35a81c9d-ac9b-412a-808e-7b718b6d0170') as case:
            # 4.2. After Search
            # 4.2.2. Preview > Stop Button
            # Can stop the preview
            case.result = download_from_shutterstock_page.music.click_stop()

        with uuid('d33a9eaa-3752-464e-8567-9608756c22a8') as case:
            # 4.2. After Search
            # 4.2.4. [Library menu] > Increasing / Decreasing
            # Select sort feature by click Name/Artist/Genre/Length/Tempo item (Not using [Sort By] drop down menu)
            check_result_1 = download_from_shutterstock_page.music.is_ascending(index=0)
            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_4_2_4-1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_4_2_4-1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.music.menu_table_header_view, file_name=image_full_path)
            check_result_2 = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.8)
            case.result = check_result_1 and check_result_2

        with uuid('1d44a96b-6dc7-452f-a3c4-f9c2b4c9ddf2') as case:
            # 4.2. After Search
            # 4.2.4. [Library menu] > [Sort by] > [Artist]
            # Can be sorted by artist normally
            download_from_shutterstock_page.music.set_sort_by(1)  # sort by artist

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_4_2_4-3.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_4_2_4-3.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.music.menu_table_header_view, file_name=image_full_path)
            check_result = download_from_shutterstock_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('651d3160-ad86-49ce-95e7-ed0fc3fa7ec7') as case:
            # 4.2. After Search
            # 4.2.4. [Library menu] > [Sort by] > [Length]
            # Can be sorted by length normally
            download_from_shutterstock_page.music.set_sort_by(2)  # sort by length

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_4_2_4-4.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_4_2_4-4.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.music.menu_table_header_view, file_name=image_full_path)
            check_result = download_from_shutterstock_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('9d500ca1-03c6-44c2-a69b-ff05016f8211') as case:
            # 4.2. After Search
            # 4.2.4. [Library menu] > [Sort by] > [Tempo]
            # Can be sorted by tempo normally
            download_from_shutterstock_page.music.set_sort_by(3)  # sort by BPM(tempo)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_4_2_4-5.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_4_2_4-5.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.music.menu_table_header_view, file_name=image_full_path)
            check_result = download_from_shutterstock_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('814b787b-f8e8-4f02-9345-30e5ffeb125c') as case:
            # 4.2. After Search
            # 4.2.4. [Library menu] > [Sort by] > [Name]
            # Can be sorted by name normally
            download_from_shutterstock_page.music.set_sort_by(0)  # sort by name

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_4_2_4-6.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_4_2_4-6.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.music.menu_table_header_view, file_name=image_full_path)
            check_result = download_from_shutterstock_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('97fe0d5e-b7dd-4032-b19a-924f77cd9a70') as case:
            # 4.2. After Search
            # 4.2.4. [Library menu] > Highlight
            # Can select (Highlight) single file by clicking the file
            download_from_shutterstock_page.music.select_song('Cozy Evening')

            check_available_music = download_from_shutterstock_page.music.check_music_icon_number()
            check_result = False if not check_available_music > 3 else True
            case.result = check_result

        with uuid('fc8846c7-7ee3-40b6-90aa-8fda8bd233af') as case:
            # 4.2. After Search
            # 4.2.5. [Download] > Select file
            # Button is enabled
            button_status = download_from_shutterstock_page.is_enabled_download()
            case.result = False if not button_status else True

        with uuid('75bbb4db-8bdd-441e-9ef1-d6365417f660') as case:
            # 4.2. After Search
            # 4.2.5. [Download] > Progress bar/ Percent
            # Show "Downloading Files[#%]"/ "Remaining Time:" normally
            download_from_shutterstock_page.click_download()
            case.result = download_from_shutterstock_page.download.verify_progress()

        with uuid('53389f04-94f0-467a-b4e5-f9e632e74075') as case:
            # 4.2. After Search
            # 4.2.5. [Download] > [Cancel]
            # Cancel downloading
            check_result_1 = download_from_shutterstock_page.download.click_cancel()
            time.sleep(DELAY_TIME)
            check_result_2 = not (download_from_shutterstock_page.download.has_dialog())

            case.result = check_result_1 and check_result_2

        with uuid('b5a6a79d-36a8-4a84-9db7-4d645bd3246d') as case:
            # 4.2. After Search
            # 4.2.5. [Download] > complete > Dialog
            # Pop up a dialog "The clips are successfully downloaded and…"
            download_from_shutterstock_page.click_download()

            case.result = download_from_shutterstock_page.is_exist(
                {'AXIdentifier': 'IDD_CLALERT', 'AXRoleDescription': 'dialog'}, timeout=10)

            download_from_shutterstock_page.download.click_complete_ok()
            time.sleep(DELAY_TIME * 10)
            download_from_shutterstock_page.click_close()
            time.sleep(DELAY_TIME)

        with uuid('037b0a6c-59f3-44c4-ba01-fbdb03135390') as case:
            # 4.2. After Search
            # 4.2.5. [Download] > complete
            # Downloaded clips are available in the media library
            case.result = media_room_page.select_media_content('Cozy Evening_548552')

            # remove downloaded content
            time.sleep(DELAY_TIME)
            media_room_page.hover_library_media('Cozy Evening_548552')
            media_room_page.right_click()
            media_room_page.select_right_click_menu('Remove from Disk')
            media_room_page.exist_click(L.media_room.confirm_dialog.btn_yes)

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        with uuid('88c41325-307b-4936-9fd1-ab95ac465e34') as case:
            # 4.3. Popular Music Search
            # 4.3.1. Four seasons
            # Check the search result whether is matched keyword or not
            media_room_page.import_media_from_shutterstock()
            time.sleep(4)
            gettyimage_page.switch_to_SS()
            time.sleep(4)
            # waiting for shutterstock enable
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=10)
            download_from_shutterstock_page.switch_to_music()
            download_from_shutterstock_page.find(L.download_from_shutterstock.music.table_clip, timeout=10)
            download_from_shutterstock_page.search.search_text('four seasons')
            download_from_shutterstock_page.find(L.download_from_shutterstock.music.table_clip, timeout=10)
            time.sleep(DELAY_TIME * 5)

            check_available_music = download_from_shutterstock_page.music.check_music_icon_number()
            check_result = False if not check_available_music >= 1 else True
            case.result = check_result

        with uuid('fbd12d8a-ab99-43e0-beb9-c928821cb2bb') as case:
            # 4.3. Popular Music Search
            # 4.3.2. Flower Road
            # Check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('flower road')
            download_from_shutterstock_page.find(L.download_from_shutterstock.music.frame_scroll_view, timeout=10)
            time.sleep(DELAY_TIME * 5)

            check_available_music = download_from_shutterstock_page.music.check_music_icon_number()
            check_result = False if not check_available_music >= 1 else True
            case.result = check_result

        with uuid('7a1e2209-c319-4f6d-878f-1a20feec529b') as case:
            # 4.3. Popular Music Search
            # 4.3.3. That One Day
            # Check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('that one day')
            download_from_shutterstock_page.find(L.download_from_shutterstock.music.frame_scroll_view, timeout=10)
            time.sleep(DELAY_TIME * 5)

            check_available_music = download_from_shutterstock_page.music.check_music_icon_number()
            check_result = False if not check_available_music >= 1 else True
            case.result = check_result

        with uuid('fc040b61-c062-4762-8217-ab293a2110ae') as case:
            # 4.3. Popular Music Search
            # 4.3.4. Time to Feel Good
            # Check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('time to feel good')
            download_from_shutterstock_page.find(L.download_from_shutterstock.music.frame_scroll_view, timeout=10)
            time.sleep(DELAY_TIME * 5)

            check_available_music = download_from_shutterstock_page.music.check_music_icon_number()
            check_result = False if not check_available_music >= 1 else True
            case.result = check_result

        with uuid('2cdb2f33-648a-40d7-9ffd-8369c00d72b4') as case:
            # 4.3. Popular Music Search
            # 4.3.5. Childish Prank
            # Check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('childish prank')
            download_from_shutterstock_page.find(L.download_from_shutterstock.music.frame_scroll_view, timeout=10)
            time.sleep(DELAY_TIME * 5)

            check_available_music = download_from_shutterstock_page.music.check_music_icon_number()
            check_result = False if not check_available_music >= 1 else True
            case.result = check_result

        with uuid('1fd13486-1fa3-431c-82ba-8eab313223c3') as case:
            # 4.3. Popular Music Search
            # 4.3.6. Above the Heavens
            # Check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('above the heavens')
            download_from_shutterstock_page.find(L.download_from_shutterstock.music.frame_scroll_view, timeout=10)
            time.sleep(DELAY_TIME * 5)

            check_available_music = download_from_shutterstock_page.music.check_music_icon_number()
            check_result = False if not check_available_music >= 1 else True
            case.result = check_result

        with uuid('c62df722-9716-4b7b-a308-f2417c8dacec') as case:
            # 4.3. Popular Music Search
            # 4.3.7. Cheerful Heart
            # Check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('cheerful heart')
            download_from_shutterstock_page.find(L.download_from_shutterstock.music.frame_scroll_view, timeout=10)
            time.sleep(DELAY_TIME * 5)

            check_available_music = download_from_shutterstock_page.music.check_music_icon_number()
            check_result = False if not check_available_music >= 1 else True
            case.result = check_result

        with uuid('26df0d08-0eb4-4fa5-adad-c584b2700335') as case:
            # 4.3. Popular Music Search
            # 4.3.8. With Hope
            # Check the search result whether is matched keyword or not
            time.sleep(DELAY_TIME * 2)
            download_from_shutterstock_page.search.search_text('with hope')
            download_from_shutterstock_page.find(L.download_from_shutterstock.music.frame_scroll_view, timeout=10)
            time.sleep(DELAY_TIME * 5)

            check_available_music = download_from_shutterstock_page.music.check_music_icon_number()
            check_result = False if not check_available_music >= 1 else True
            case.result = check_result

        with uuid('ec31398d-f3b5-4614-9e0d-3e16731e5e07') as case:
            # 4.3. Popular Music Search
            # 4.3.9. I'm in Love
            # Check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('i'+"'"+'m in love')
            download_from_shutterstock_page.find(L.download_from_shutterstock.music.frame_scroll_view, timeout=10)
            time.sleep(DELAY_TIME * 5)

            check_available_music = download_from_shutterstock_page.music.check_music_icon_number()
            check_result = False if not check_available_music >= 1 else True
            case.result = check_result

        with uuid('b4233ca8-316c-4fcd-9b33-aa902a55077e') as case:
            # 4.3. Popular Music Search
            # 4.3.10. Urban Chill
            # Check the search result whether is matched keyword or not
            download_from_shutterstock_page.search.search_text('urban chill')
            download_from_shutterstock_page.find(L.download_from_shutterstock.music.frame_scroll_view, timeout=10)
            time.sleep(DELAY_TIME * 5)

            check_available_music = download_from_shutterstock_page.music.check_music_icon_number()
            check_result = False if not check_available_music >= 1 else True
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        with uuid('be9fd9ff-55f5-4a91-9ba7-73a81f8f7f67') as case:
            # 5. Advanced Test
            # 5.1. Search & Download
            # 5.1.1. Search result > Launch PDR with [ENG] and input keyword "sports car"
            # Using different languages to input keyword and check the search result
            media_room_page.import_media_from_shutterstock()
            time.sleep(4)
            gettyimage_page.switch_to_SS()
            time.sleep(4)
            # waiting for shutterstock enable
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=10)
            time.sleep(DELAY_TIME * 3)
            download_from_shutterstock_page.search.search_text('sports car')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_5_1_1-1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_5_1_1-1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_scroll_view, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.7)

        with uuid('901482a3-5d83-4c1b-8010-ad81d56e7603') as case:
            # 5.1. Search & Download
            # 5.1.1. Search result > Launch PDR with [CHT] and input keyword "跑車"
            # Using different languages to input keyword and check the search result
            download_from_shutterstock_page.search.search_text('跑車')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=20)
            time.sleep(DELAY_TIME * 3)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_5_1_1-2.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_5_1_1-2.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_scroll_view, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.7)

        with uuid('78076421-4463-44e8-8148-ed7507407656') as case:
            # 5.2. Error Handling
            # 5.2.3. No match result >input keyword in Search Box
            # Show "No clips matched the search."
            download_from_shutterstock_page.search.search_text('zzzzz')
            #download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=5)
            time.sleep(DELAY_TIME*7)

            image_full_path = Auto_Ground_Truth_Folder + 'shutterstock_5_2_3-1.png'
            ground_truth = Ground_Truth_Folder + 'shutterstock_5_2_3-1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.frame_scroll_view, file_name=image_full_path)
            check_result_1 = download_from_shutterstock_page.compare(ground_truth, current_preview)

            check_result_2 = download_from_shutterstock_page.click_search_not_found_ok()
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    c986fec5-73e1-4e27-8d32-304176f80664
                    
                    
                    f1a15a2c-13b0-4384-8866-e8b385315600
                    7cb36a0e-fa65-49aa-a26d-3d5e419dd784
                    8bea3a4b-7fcf-4b2e-8b59-1209361f7757
                    d58abd2f-7afb-4543-9203-97c4eb6c8d1e
                    ca3879a3-f38b-45d1-9878-fa54453e860c
                    7a4c7a1b-271b-4525-9552-6319b416ed13
                    893fed29-c12f-4f59-8616-b73125a9f3ba
                    b27fa92e-2658-4cb3-9329-110cecbdb693
                    038d7dc9-f221-412f-b756-54a413a9cd5d
                    4e8bfa76-abf3-498e-ae5c-ddae182d8405
                    be160f70-66c4-4ef4-977d-83f2b3d22e8f
                    270cb548-5071-46c8-9cee-f6fe9f3e7d2a
                    27aa47ab-7862-4184-af48-1f8031762143
                    ae7e43e5-f753-4269-aef1-54da67c7a3a6
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'

        with uuid('ce38e68f-e794-48c5-ad48-3e0e9d3f43e1') as case:
            # 4.1. Before Search
            # 4.1.4. List Panel > Music tooltip > hover
            # show detail profile information
            '''
            # 2022-03-23 AT skipped case ("Genre" content changes frequently)
            download_from_shutterstock_page.music.hover_song('1001 Nights')
            case.result = download_from_shutterstock_page.music.verify_song_tooltip(
                Ground_Truth_Folder + 'shutterstock_4_1_4-7.png', '1001 Nights')
            '''
            case.result = None
            case.fail_log = '*SKIP by AT*'

        with uuid('b3356efa-c95f-487c-a8bd-d3cefecce3c2') as case:
            # 4.2. After Search
            # 4.2.4. [Library menu] > Tooltip
            # Show "Name, Artist, Genre, Length & Tempo" about this file
            '''
            # 2022-03-23 AT skipped case ("Genre" content changes frequently)
            download_from_shutterstock_page.music.hover_song('Cozy Evening')
            case.result = download_from_shutterstock_page.music.verify_song_tooltip(
                Ground_Truth_Folder + 'shutterstock_4_2_4-7.png', 'Cozy Evening')
            '''
            case.result = None
            case.fail_log = '*SKIP by AT*'