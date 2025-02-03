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
base_page = PageFactory().get_page_object('base_page', mac)
media_room_page = PageFactory().get_page_object('media_room_page', mac)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mac)
playback_window_page = PageFactory().get_page_object('playback_window_page', mac)
precut_page = PageFactory().get_page_object('precut_page', mac)
tips_area_page = PageFactory().get_page_object('tips_area_page', mac)
library_preview_page = PageFactory().get_page_object('library_preview_page', mac)
title_designer_page = PageFactory().get_page_object('title_designer_page', mac)
pan_zoom_page = PageFactory().get_page_object('pan_zoom_page', mac)
blending_mode_page = PageFactory().get_page_object('blending_mode_page', mac)
fix_enhance_page = PageFactory().get_page_object('fix_enhance_page', mac)
effect_room_page = PageFactory().get_page_object('effect_room_page', mac)
crop_zoom_pan_page = PageFactory().get_page_object('crop_zoom_pan_page', mac)
video_speed_page = PageFactory().get_page_object('video_speed_page', mac)
pip_designer_page = PageFactory().get_page_object('pip_designer_page', mac)
video_collage_designer_page = PageFactory().get_page_object('video_collage_designer_page', mac)
transition_room_page = PageFactory().get_page_object('transition_room_page', mac)
download_from_shutterstock_page = PageFactory().get_page_object('download_from_shutterstock_page', mac)
gettyimage_page = PageFactory().get_page_object('gettyimage_page', mac)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mac, html_name="GettyImage.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
#Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/GroundTruth/Pre_Cut/'
#Auto_Ground_Truth_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/SFT/ATGroundTruth/Pre_Cut/'
#Test_Material_Folder = '/Users/qadf_at/Desktop/Jamie/AT/SFT_20210302/Material/'
Ground_Truth_Folder = app.ground_truth_root + '/gettyimage/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/gettyimage/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

class Test_Gettyimage():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME*4)
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
            google_sheet_execution_log_init('gettyimage')

    @classmethod
    def teardown_class(cls):

        logger('teardown_class - export report')
        report.export()
        logger(
            f"effect_setting_from_i_button_menu result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()


    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        #Video > After search
        with uuid('54d1bed6-78ca-4855-a573-21781511cc05') as case:
            #Hover the thumbnail then click the heart icon
            media_room_page.import_media_from_shutterstock()
            time.sleep(DELAY_TIME * 8)
            # waiting for shutterstock ready
            gettyimage_page.switch_to_GI()
            gettyimage_page.handle_what_is_stock_media()

            time.sleep(DELAY_TIME * 8)
            download_from_shutterstock_page.search.search_text('airport')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)
            time.sleep(DELAY_TIME*3)
            download_from_shutterstock_page.set_scroll_bar(0)
            time.sleep(DELAY_TIME)
            case.result = gettyimage_page.hover_heart_icon(1)
            main_page.left_click()


        with uuid('9c007bb0a83-ef70-49a8-aa58-c60ff33ae0a3') as case:
            #Click to My Favorites tab to browse the added media
            gettyimage_page.click_my_favorites_button()
            case.result = gettyimage_page.click_heart_icon(0)

        with uuid('90a9f222-b93e-4ec6-a0eb-e77b7b45f8ca') as case:
            #Only show bundled stock for the first 6 results
            gettyimage_page.switch_to_GI()
            download_from_shutterstock_page.search.search_text('airport')
            time.sleep(DELAY_TIME)
            download_from_shutterstock_page.photo.click_thumbnail(0)
            result0 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(0)
            download_from_shutterstock_page.photo.click_thumbnail(1)
            result1 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(1)
            download_from_shutterstock_page.photo.click_thumbnail(2)
            result2 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(2)
            download_from_shutterstock_page.photo.click_thumbnail(3)
            result3 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(3)
            download_from_shutterstock_page.photo.click_thumbnail(4)
            result4 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(4)
            download_from_shutterstock_page.photo.click_thumbnail(5)
            result5 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(5)
            case.result = result0 and result1 and result2 and result3 and result4 and result5

        with uuid('b1bdd6a2-ff2a-4ed8-b1da-57f86aff73a7') as case:
            #Show 1/3 premium stock after the first 6 like Pay > Free > Free> Pay > Free > Free> ….
            time.sleep(2)
            download_from_shutterstock_page.photo.click_thumbnail(6)
            result0 = gettyimage_page.return_add_to_cart_button_status()
            time.sleep(0.5)
            download_from_shutterstock_page.photo.click_thumbnail(6)
            download_from_shutterstock_page.photo.click_thumbnail(7)
            result1 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            time.sleep(0.5)
            download_from_shutterstock_page.photo.click_thumbnail(7)
            download_from_shutterstock_page.photo.click_thumbnail(8)
            time.sleep(0.5)
            result2 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(8)
            download_from_shutterstock_page.photo.click_thumbnail(9)
            time.sleep(0.5)
            result3 = gettyimage_page.return_add_to_cart_button_status()
            download_from_shutterstock_page.photo.click_thumbnail(9)
            download_from_shutterstock_page.photo.click_thumbnail(10)
            time.sleep(0.5)
            result4 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(10)
            download_from_shutterstock_page.photo.click_thumbnail(11)
            time.sleep(0.5)
            result5 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(11)
            case.result = result0 and result1 and result2 and result3 and result4 and result5

        with uuid('f8affcc2-2206-476a-9d27-d4aa275f15de') as case:
            #Check the ? items are right
            download_from_shutterstock_page.photo.click_thumbnail(6)
            gettyimage_page.click_add_to_cart_button()
            case.result = True if main_page.exist(L.gettyimage.bubble_proceed_to_checkout).AXTitle == "Proceed to Checkout\n(1 item(s))" else False

        with uuid('ccad80b5-c614-4f64-b0ac-a9f0d549bcd9') as case:
            #Show the message "Added to cart" for 3 sec
            current_result = main_page.is_exist(L.gettyimage.bubble_cart)
            time.sleep(4)
            current_result2 = main_page.is_not_exist(L.gettyimage.bubble_cart)
            case.result = current_result and current_result2

        with uuid('b6c7baaa-8d7a-4d33-a170-67ccf1a01774') as case:
            #PC: Click to open browser to AK’s page and pop up waiting dialog
            gettyimage_page.click_add_to_cart_button()
            case.result = gettyimage_page.click_bubble_proceed_checkout()

        with uuid('7d9e07a4-5daf-4bb2-8a6c-5844eb163f1d') as case:
            #Mac: Proceed the IAP flow
            time.sleep(5)
            case.result = gettyimage_page.handle_checkout_is_complete_dialog('cancel')

        with uuid('b81614db-0737-4137-82f6-a19f5dfba4a3') as case:

            # Download a free media and add a pay media to cart
            download_from_shutterstock_page.photo.click_thumbnail(7)
            current_result2 = download_from_shutterstock_page.click_download()
            time.sleep(10)
            download_from_shutterstock_page.download.hd_video.click_no()
            download_from_shutterstock_page.download.click_complete_ok()
            time.sleep(10)
            current_result = gettyimage_page.click_shopping_cart_button()
            case.result = current_result and current_result2

        with uuid('9d06def1-8116-49a0-a4a1-7530f9152985') as case:
            # "Added to cart" message > Pop up shopping cart dialog
            time.sleep(2)
            case.result = gettyimage_page.is_enter_shopping_cart_window()

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        with uuid("7a4ee8e8-9f0e-4a1f-9b5f-5584e1ea273d") as case:
            #[ Import media ] > [ Download Media from Shutterstock and Getty images]
            media_room_page.import_media_from_shutterstock()
            case.result = download_from_shutterstock_page.is_in_shutterstock()
            time.sleep(8)  # waiting for all clips index ready
            gettyimage_page.switch_to_GI()
            gettyimage_page.handle_what_is_stock_media()

        with uuid('e8b2a258-ba1b-464e-a470-867726096236') as case:
            #Check Video/Photo preview with default browser
            download_from_shutterstock_page.video.hover_thumbnail(0)
            main_page.mouse.click()
            time.sleep(2)
            #case.result = main_page.check_chrome_page()
            case.result = download_from_shutterstock_page.close_pop_up_preview_window()

        with uuid('5b24b2ec-c4bd-429e-8874-3064f8cd2041') as case:
            #Check My Favorites
            gettyimage_page.click_my_favorites_button()
            case.result = main_page.exist(L.gettyimage.no_favorite_msg)

        with uuid('af807e5b-e0b8-4910-8e19-26195bdaf7bb') as case:
            #Check Purchased
            gettyimage_page.click_purchased_button()
            case.result = main_page.exist(L.gettyimage.btn_purchased).AXEnabled

        with uuid('868fae7c-8cf8-4354-85c4-d2266dfb6492') as case:
            #Check Downloaded
            gettyimage_page.click_downloaded_button()
            case.result = main_page.exist(L.gettyimage.btn_download).AXEnabled

        with uuid('cffb30de-908d-11ec-b909-0242ac120002') as case:
            #Check Shopping cart > Disabled when nothing in shopping cart
            case.result = not main_page.exist(L.gettyimage.btn_cart).AXEnabled

        with uuid('9055ec81-acbb-4e0b-8b16-b9f3e5e3cbd7') as case:
            #Check Shopping cart
            gettyimage_page.switch_to_GI()
            download_from_shutterstock_page.video.click_thumbnail(6)
            gettyimage_page.click_add_to_cart_button()
            gettyimage_page.click_shopping_cart_button()
            case.result = gettyimage_page.is_enter_shopping_cart_window()
            main_page.press_esc_key()

        with uuid('eed1b650-d076-4af3-a308-7c8cfc7f8017') as case:
            #Check Filter > Click first
            gettyimage_page.click_filter_button()
            case.result = main_page.exist(L.gettyimage.video.scroll_bar_filter)

        with uuid('071058ab-ef7f-4d5b-944b-e3d4b06bdd64') as case:
            #Check Filter > Close arrow "<"
            gettyimage_page.click_filter_explorer_view()
            case.result = not main_page.exist(L.gettyimage.video.scroll_bar_filter)

        with uuid('2ee557a8-4e3c-4653-ae26-cec32fffe2c3') as case:
            #Check Filter > Click again
            gettyimage_page.click_filter_button()
            gettyimage_page.click_filter_button()
            case.result = not main_page.exist(L.gettyimage.video.scroll_bar_filter)


        with uuid('d4d9c18d-cff5-470a-a0c6-c004f59a07f0') as case:
            # 1.6. Scroll bar
            # 1.6.1. Default status
            # enable scroll bar
            case.result = download_from_shutterstock_page.is_exist(L.download_from_shutterstock.scroll_media)

        with uuid("00bc32fb-3674-4cb7-ab78-466a741fedda") as case:
            #[X]
            download_from_shutterstock_page.click_close()
            time.sleep(2)
            case.result = not (download_from_shutterstock_page.is_in_shutterstock())

        with uuid('7e8a76d3-87f0-4950-b1d0-c4c7833fceab') as case:
            #[ Download From ] > [ Download Media from Shutterstock and Getty images]
            media_room_page.collection_view_deselected_media()
            media_room_page.right_click()
            media_room_page.select_right_click_menu(
                'Download from', 'Download Media from Shutterstock and Getty Images...')
            time.sleep(DELAY_TIME*3)
            gettyimage_page.switch_to_SS()
            time.sleep(DELAY_TIME * 3)
            case.result = download_from_shutterstock_page.is_in_shutterstock()


            time.sleep(8)  # waiting for all clips index ready
            gettyimage_page.switch_to_GI()

        with uuid('4aeb13aa-53fb-4293-bd3c-b4bb4b0438be') as case:
            # 1.2. Caption Bar
            # 1.2.1. General Functions > [Maximize] Button > Maximize
            current_reuslt = download_from_shutterstock_page.click_maximize()
            image_full_path = Auto_Ground_Truth_Folder + '1_1_1.jpg'
            ground_truth = Ground_Truth_Folder + '1_1_1.jpg'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            download_from_shutterstock_page.compare(ground_truth, current_preview)
            case.result = current_reuslt

        with uuid('8c43fedd-a73d-430d-b446-65c9b362d329') as case:
            # 1.2. Caption Bar
            # 1.2.1. General Functions > [Restore down] Button > Restore down
            current_reuslt = download_from_shutterstock_page.click_maximize()
            image_full_path = Auto_Ground_Truth_Folder + '1_1_2.jpg'
            ground_truth = Ground_Truth_Folder + '1_1_2.jpg'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            download_from_shutterstock_page.compare(ground_truth, current_preview)
            case.result = current_reuslt

        with uuid('6e7f4fd2-98a9-4d1f-8a49-af71385a255a') as case:
            # 1.2. Caption Bar
            # 1.2.2. Caption Name > Download Media from Shutterstock
            # display "Download Media from Shutterstock" on the caption bar
            caption_title_text = download_from_shutterstock_page.get_caption_title()

            logger(caption_title_text)
            case.result = False if not caption_title_text == 'Download Media from Shutterstock and Getty Images' \
                else True

        with uuid('40c942d1-6221-4026-bdaa-bfbeeced66f7') as case:
            # 1.4. Preview
            # 1.4.1. Thumbnail > Default thumbnail (From Other Entrance)
            # check(Video/Photo) thumbnail preview gray, black or not
            image_full_path = Auto_Ground_Truth_Folder + '1_1_3.jpg'
            ground_truth = Ground_Truth_Folder + '1_1_3.jpg'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.btn_photo_tab, file_name=image_full_path)
            check_result_1 = download_from_shutterstock_page.compare(ground_truth, current_preview)

            download_from_shutterstock_page.switch_to_video()
            time.sleep(DELAY_TIME * 8)
            image_full_path = Auto_Ground_Truth_Folder + '1_1_4.jpg'
            ground_truth = Ground_Truth_Folder + '1_1_4.jpg'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.btn_video_tab, file_name=image_full_path)
            check_result_2 = download_from_shutterstock_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('fb262646-77f4-4cbf-92ab-486c028db2c3') as case:
            # 1.4. Preview
            # 1.4.2. Preview icon
            # check(Video/Photo) preview icon truncate or not

            case.result = check_result_1 and check_result_2

        with uuid('a21b9236-874b-4e99-b3f8-bc7248749538') as case:
            # 1.5. [i] button
            # 1.5.1. Cannot show (i button) in below
            case.result = not download_from_shutterstock_page.is_exist(L.download_from_shutterstock.btn_i)

        with uuid('cfe1ce75-abc4-48ec-8308-b2b55ffb1cf8') as case:
            # 1.7. Previous/Next Page
            # 1.7.1. Next Page > Tooltip
            # next page
            download_from_shutterstock_page.hover_next_page()
            time.sleep(DELAY_TIME * 2)
            case.result = download_from_shutterstock_page.verify_next_page_tooltip(
                ground_truth=Ground_Truth_Folder + '1_1_6.jpg')

        with uuid('9c4f72d5-c45d-4713-b871-e61f7906e811') as case:
            # 1.7. Previous/Next Page
            # 1.7.1. Next Page > Next Page > button
            # go to next page if click ">" button
            case.result = download_from_shutterstock_page.click_next_page()
            time.sleep(DELAY_TIME * 2)

        with uuid('3deda7a3-0247-41c3-bcc9-0e48673dc580') as case:
            # 1.7. Previous/Next Page
            # 1.7.2. Previous Page > Tooltip
            # previous page
            download_from_shutterstock_page.hover_previous_page()
            time.sleep(DELAY_TIME * 2)
            case.result = download_from_shutterstock_page.verify_previous_page_tooltip(
                ground_truth=Ground_Truth_Folder + '1_1_8.jpg')

        with uuid('353893eb-3961-4ff0-aac5-b3364605ebdd') as case:
            # 1.7. Previous/Next Page
            # 1.7.2. Previous Page > Previous Page > button
            # go to previous page if click "<" button
            case.result = download_from_shutterstock_page.click_previous_page()
            time.sleep(2)

        with uuid('64758f79-c7a1-493e-b0af-68a01370d527') as case:
            # 1.2. Caption Bar
            # 1.2.1. General Functions > [Esc] > Hotkey
            # close the download media from shutterstock window
            download_from_shutterstock_page.press_esc_key()  # unselect on search box
            download_from_shutterstock_page.press_esc_key()
            time.sleep(DELAY_TIME)
            case.result = not (download_from_shutterstock_page.is_in_shutterstock())


        with uuid('b3e30fbc-7aeb-4115-8c0f-1a07c34c7a64') as case:
            # 1.1 Entrance
            # 1.1.3. Media Room > [Premium Media]
            # pop up the download media from shutterstock window
            media_room_page.hover_library_media('Stock Content')
            time.sleep(DELAY_TIME)
            media_room_page.double_click()
            case.result = download_from_shutterstock_page.is_in_shutterstock()

            time.sleep(DELAY_TIME * 8)  # waiting for all clips index ready
            gettyimage_page.switch_to_GI()

        with uuid('fcf75372-4a74-4b68-b178-1b08ce0e624e') as case:
            # Default window size
            image_full_path = Auto_Ground_Truth_Folder + '1_1_13.jpg'
            ground_truth = Ground_Truth_Folder + '1_1_13.jpg'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview, similarity=0.8)


        with uuid('d94dd8a3-6456-4c23-936f-e1e327077894') as case:
            # 1.6. Scroll bar
            # 1.6.2. Check scroll bar >Resize Icon then Check Scroll bar status
            # if thumbnail size > default size, it will enable scroll bar
            image_full_path = Auto_Ground_Truth_Folder + '1_1_14.jpg'
            ground_truth = Ground_Truth_Folder + '1_1_14.jpg'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.scroll_media, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview)


        with uuid('85e694b2-2492-43d3-bbd8-9609b43497d5') as case:
            # 1.2. Caption Bar
            # 1.2.1. General Functions > Adjust window size
            # resize by dragging the window

            case.result = download_from_shutterstock_page.adjust_window(x=325, y=61, w=949, h=747)

        with uuid('a630b98a-bff1-43ad-af12-815ae1efc721') as case:
            # 1.6. Scroll bar
            # 1.6.2. Check scroll bar > Adjust windows size
            # resize the window then check scroll bar status
            image_full_path = Auto_Ground_Truth_Folder + '1_1_11.jpg'
            ground_truth = Ground_Truth_Folder + '1_1_11.jpg'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.scroll_media, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview)

        with uuid('1f8fb665-0148-4bc3-9497-9f1465258e23') as case:
            # 1.2. Caption Bar
            # 1.2.1. General Functions > Adjust window size then close > Open again
            # reopen to keep the previous size
            download_from_shutterstock_page.click_close()
            time.sleep(DELAY_TIME)
            media_room_page.import_media_from_shutterstock()
            time.sleep(DELAY_TIME * 8)
            gettyimage_page.click_my_favorites_button()

            image_full_path = Auto_Ground_Truth_Folder + '1_1_12.jpg'
            ground_truth = Ground_Truth_Folder + '1_1_12.jpg'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.download_from_shutterstock.window, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview)

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid('4e32754e-8a01-4b24-8f96-384f7ca2cf07') as case:
            # 2. Video
            # 2.1. Before Search
            # 2.1.1. Search box > Default text
            # show "search" / empty in the search box
            media_room_page.import_media_from_shutterstock()
            time.sleep(DELAY_TIME * 8)
            # waiting for shutterstock ready
            gettyimage_page.switch_to_GI()
            gettyimage_page.handle_what_is_stock_media()
            case.result = download_from_shutterstock_page.search.verify_default_string(default='Search')

            time.sleep(DELAY_TIME * 8)

        with uuid('5667d5be-5ad6-4374-bfe5-587b9d04447e') as case:
            # 2.1. Before Search
            # 2.1.1. Search box > Tooltip
            # show "Search"
            case.result = download_from_shutterstock_page.search.verify_tooltip(
                Ground_Truth_Folder + '1_2_1.jpg')
            time.sleep(2)

        with uuid('a7e1a949-bab0-4b6b-9287-d85e937b3b8c') as case:
            # 2.1. Before Search
            # 2.1.2. Library menu > Default Icons size > [Medium icons]
            # thumbnails show as medium icons. one page has 30 icons
            time.sleep(10)
            download_from_shutterstock_page.set_library_setting('Small')
            time.sleep(5)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 29})
            #check_result_2 = not main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 30})
            case.result = check_result_1# and check_result_2
            download_from_shutterstock_page.set_library_setting('Medium')
            time.sleep(2)

        with uuid('6c46c463-9b4d-4ca8-88e0-17f2820e9b43') as case:
            # 2.1. Before Search
            # 2.1.3. Page number > Current Page number
            # default value is "1"
            current_page_amount = download_from_shutterstock_page.get_page_amount()
            logger(current_page_amount)
            case.result = False if not current_page_amount == 1 else True

        with uuid('e309ebb6-4c6b-4694-a5a4-748392455ce8') as case:
            # 2.1. Before Search
            # 2.1.3. Page number > Total Page number
            # total page number
            time.sleep(10)
            total_page_amount = download_from_shutterstock_page.get_total_page_amount()
            logger(total_page_amount)
            case.result = False if not total_page_amount == 40 else True

        with uuid('f4eed37f-ba00-408f-98f0-119c2c1ec26b') as case:
            # 2.1. Before Search
            # 2.1.4. [Download] > Default status
            # button is disable
            button_status = download_from_shutterstock_page.is_enabled_download()
            case.result = True if not button_status else False

        with uuid('8d06cd62-ca2f-4e5e-9a22-644f5a3248a8') as case:
            # 2.1. Before Search
            # 2.1.4. [Download] > Tooltip
            # show "Download"
            case.result = download_from_shutterstock_page.verify_download_tooltip(
                Ground_Truth_Folder + '1_2_2.jpg')

        with uuid('5d3a84d0-bc69-4e35-a949-ac5a6c9b7275') as case:
            # 2.1. Before Search
            # 2.1.5. Selected clip(s) > Default value
            # show "0 clips"
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            case.result = False if not selected_amount == 0 else True

        with uuid('7184f33a-a31e-42be-a53d-d05c2afc155c') as case:
            #Hover the thumbnail then click the heart icon
            case.result = gettyimage_page.hover_heart_icon(0)
            main_page.left_click()

        with uuid('9c000d85-8fc7-4416-854a-462a18722f90a') as case:
            #Click to My Favorites tab to browse the added media
            gettyimage_page.click_my_favorites_button()
            case.result = gettyimage_page.click_heart_icon(0)

        with uuid('2624b25a-10f7-46f8-9305-5f5e8acbff3b') as case:
            #Only show bundled stock for the first 6 results
            gettyimage_page.switch_to_GI()
            download_from_shutterstock_page.photo.click_thumbnail(0)
            result0 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(0)
            download_from_shutterstock_page.photo.click_thumbnail(1)
            result1 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(1)
            download_from_shutterstock_page.photo.click_thumbnail(2)
            result2 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(2)
            download_from_shutterstock_page.photo.click_thumbnail(3)
            result3 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(3)
            download_from_shutterstock_page.photo.click_thumbnail(4)
            result4 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(4)
            download_from_shutterstock_page.photo.click_thumbnail(5)
            result5 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(5)
            case.result = result0 and result1 and result2 and result3 and result4 and result5

        with uuid('ac7127f1-e6bc-46f2-8ed6-6d951ee2a140') as case:
            #Show 1/3 premium stock after the first 6 like Pay > Free > Free> Pay > Free > Free> ….
            download_from_shutterstock_page.set_scroll_bar(0.2)
            download_from_shutterstock_page.photo.click_thumbnail(6)
            result0 = gettyimage_page.return_add_to_cart_button_status()
            download_from_shutterstock_page.photo.click_thumbnail(6)
            download_from_shutterstock_page.photo.click_thumbnail(7)
            result1 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(7)
            download_from_shutterstock_page.photo.click_thumbnail(8)
            result2 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(8)
            download_from_shutterstock_page.set_scroll_bar(0.4)
            download_from_shutterstock_page.photo.click_thumbnail(9)
            result3 = gettyimage_page.return_add_to_cart_button_status()
            download_from_shutterstock_page.photo.click_thumbnail(9)
            download_from_shutterstock_page.photo.click_thumbnail(10)
            result4 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(10)
            download_from_shutterstock_page.photo.click_thumbnail(11)
            result5 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(11)
            case.result = result0 and result1 and result2 and result3 and result4 and result5

        with uuid('7dc228af-5e05-44ec-8221-3513e5cb9e19') as case:
            #Check the ? items are right
            download_from_shutterstock_page.photo.click_thumbnail(6)
            gettyimage_page.click_add_to_cart_button()
            case.result = True if main_page.exist(L.gettyimage.bubble_proceed_to_checkout).AXTitle == "Proceed to Checkout\n(1 item(s))" else False

        with uuid('ff6cddd5-cbf6-4653-b6a3-c1564bb2ece4') as case:
            #Show the message "Added to cart" for 3 sec
            current_result = main_page.is_exist(L.gettyimage.bubble_cart)
            time.sleep(4)
            current_result2 = main_page.is_not_exist(L.gettyimage.bubble_cart)
            case.result = current_result and current_result2

        with uuid('0c13d1de-91b2-4766-9e2d-531b82b6393f') as case:
            #PC: Click to open browser to AK’s page and pop up waiting dialog
            gettyimage_page.click_add_to_cart_button()
            time.sleep(1)
            case.result = gettyimage_page.click_bubble_proceed_checkout()

        with uuid('2c292600-09af-4c83-8dcd-6726212c8e50') as case:
            #Mac: Proceed the IAP flow
            case.result = gettyimage_page.handle_checkout_is_complete_dialog('cancel')

        with uuid('c6784e15-a75b-43e0-8be9-95374536d152') as case:
            #Download a free media and add a pay media to cart
            download_from_shutterstock_page.photo.click_thumbnail(7)
            current_result2 = download_from_shutterstock_page.click_download()
            time.sleep(10)
            download_from_shutterstock_page.download.hd_video.click_no()
            download_from_shutterstock_page.download.click_complete_ok()
            time.sleep(10)
            current_result = gettyimage_page.click_shopping_cart_button()
            case.result = current_result and current_result2

        with uuid('a30e5b16-b4dd-484f-a534-9ffeecf06fd0') as case:
            #"Added to cart" message > Pop up shopping cart dialog
            time.sleep(2)
            case.result = gettyimage_page.is_enter_shopping_cart_window()

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid('45ce7cb7-cf78-43b4-bfb2-976cb66a5e86') as case:
            #Collections > Premium ($)
            media_room_page.import_media_from_shutterstock()
            time.sleep(DELAY_TIME * 8)
            # waiting for shutterstock ready
            gettyimage_page.switch_to_GI()
            gettyimage_page.handle_what_is_stock_media()

            time.sleep(DELAY_TIME * 8)
            gettyimage_page.click_filter_button()
            current_result = gettyimage_page.filter.set_collection_type(2)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_collection_type() == 'Premium ($)' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('ea8f51d7-b71e-4c2d-b99b-a9a8e9c97675') as case:
            # Collections > 365 subscription
            current_result = gettyimage_page.filter.set_collection_type(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_collection_type() == '365 subscription' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('ce59f3c8-d3c7-4d91-8285-d65ff4b3b1c3') as case:
            # Collections > All
            current_result = gettyimage_page.filter.set_collection_type(0)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_collection_type() == 'All' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('9c5cea8d-d23a-41b6-84fe-f3ab2b3e38b6') as case:
            # Sort by > Most popular
            current_result = gettyimage_page.filter.set_sort_by_type(3)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type() == 'Most popular' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('cdcf8706-0cef-406a-adb8-f1b31100bd6a') as case:
            # Sort by > Random
            current_result = gettyimage_page.filter.set_sort_by_type(2)

            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type() == 'Random' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('2b4a6f9b-b3fd-44d4-8c74-15678c0627f4') as case:
            # Sort by > Newest
            current_result = gettyimage_page.filter.set_sort_by_type(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type() == 'Newest' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('f80db502-2673-49d5-8b22-880f44c0d9bd') as case:
            # Sort by > Best matched
            current_result = gettyimage_page.filter.set_sort_by_type(0)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type() == 'Best matched' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('e09e45df-b434-4c06-8a26-a6e4c0dc19b1') as case:
            # Duration > Longer than 1 min  ( Unable to search match media in 20.3630)
            current_result = gettyimage_page.filter.video.set_duration_type(3)
            check_result_2 = True if gettyimage_page.filter.video.get_duration_type() == 'Longer than 1 min' else False
            case.result = current_result and check_result_2 and gettyimage_page.handle_no_match_dialog()

        with uuid('bf505fa4-dfde-4873-8423-e14fa13b2acb') as case:
            # Duration > 1 min or less
            current_result = gettyimage_page.filter.video.set_duration_type(2)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.video.get_duration_type() == '1 min or less' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('18cf56b0-a29a-4798-9d72-65b483302895') as case:
            # Duration > 30s or less
            current_result = gettyimage_page.filter.video.set_duration_type(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.video.get_duration_type() == '30s or less' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('e62f8747-475d-4ced-a4fc-d20992989373') as case:
            # Duration > All
            current_result = gettyimage_page.filter.video.set_duration_type(0)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.video.get_duration_type() == 'All' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('5516db48-dbdd-45a5-b400-d95b0721b581') as case:
            # Resolution (Formats) > SD or above
            gettyimage_page.filter.set_video_scroll_bar(0.6)
            current_result = gettyimage_page.filter.video.set_resolution_type(3)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.video.get_resolution_type() == 'SD or above' else False
            case.result = current_result and check_result_1 and check_result_2


        with uuid('91c2c9f1-5ae5-44b9-824e-e24a5345941e') as case:
            # Resolution (Formats) > HD or above
            current_result = gettyimage_page.filter.video.set_resolution_type(2)

            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.video.get_resolution_type() == 'HD or above' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('6b4556de-f07b-4938-be09-0e85b8851c3d') as case:
            # Resolution (Formats) > 4K or above
            current_result = gettyimage_page.filter.video.set_resolution_type(1)

            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.video.get_resolution_type() == '4K or above' else False
            case.result = current_result and check_result_1 and check_result_2


        with uuid('a6b92369-259e-4105-b9f7-385441ff87c3') as case:
            # Resolution (Formats) > All
            current_result = gettyimage_page.filter.video.set_resolution_type(0)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.video.get_resolution_type() == 'All' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('f876ce85-7718-4ec5-98bb-d22cc7657d35') as case:
            # Composition > Close-up
            current_result = gettyimage_page.filter.video.composition.set_close_up(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.composition.get_close_up()
            case.result = current_result and check_result_1 and check_result_2
            gettyimage_page.filter.video.composition.set_close_up(0)

        with uuid('1b090837-cf43-4d37-a3ba-b6e2b04bc732') as case:
            # Composition > Looking at camera, Candid
            current_result = gettyimage_page.filter.video.composition.set_candid(1)
            current_result2 = gettyimage_page.filter.video.composition.set_looking(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.composition.get_candid()
            check_result_3 = gettyimage_page.filter.video.composition.get_looking()
            case.result = current_result and current_result2 and check_result_1 and check_result_2 and check_result_3
            gettyimage_page.filter.video.composition.set_candid(0)
            gettyimage_page.filter.video.composition.set_looking(0)

        with uuid('e8fd1f5c-aeea-48e6-bb9a-e0dd3a302dfe') as case:
            # Viewpoint > Lockdown
            gettyimage_page.filter.set_video_scroll_bar(1)
            current_result = gettyimage_page.filter.video.viewpoint.set_lockdown(1)

            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.viewpoint.get_lockdown()
            case.result = current_result and check_result_1 and check_result_2
            gettyimage_page.filter.video.viewpoint.set_lockdown(0)

        with uuid('74a0371c-ae61-41fe-a4ca-7d9979b5a919') as case:
            # Viewpoint > Panning, Tracking shot ( Unable to search match media in 20.3630)
            gettyimage_page.filter.video.viewpoint.set_panning(1)
            current_result3 = gettyimage_page.handle_no_match_dialog()
            gettyimage_page.filter.video.viewpoint.set_tracking_shot(1)
            current_result2 = gettyimage_page.handle_no_match_dialog()
            current_result = True if gettyimage_page.filter.video.viewpoint.get_panning() and gettyimage_page.filter.video.viewpoint.get_tracking_shot() == 1 else False
            case.result = current_result and current_result2 and current_result3
            gettyimage_page.filter.video.viewpoint.set_panning(0)
            gettyimage_page.handle_no_match_dialog()
            gettyimage_page.filter.video.viewpoint.set_tracking_shot(0)

        with uuid('10632a14-5fd8-4b66-a7ae-f45031e73824') as case:
            # Viewpoint > Aerial view, High angle view
            current_result = gettyimage_page.filter.video.viewpoint.set_aerial_view(1)
            current_result2 = gettyimage_page.filter.video.viewpoint.set_high_angle(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.viewpoint.get_aerial_view()
            check_result_3 = gettyimage_page.filter.video.viewpoint.get_high_angle()
            case.result = current_result and current_result2 and check_result_1 and check_result_2 and check_result_3
            gettyimage_page.filter.video.viewpoint.set_aerial_view(0)
            gettyimage_page.filter.video.viewpoint.set_high_angle(0)

        with uuid('17e5336e-5abb-4852-8d4a-4afbec9b58ab') as case:
            # Viewpoint > Low angle view, Tilt, Point of view
            current_result = gettyimage_page.filter.video.viewpoint.set_tilt(1)
            current_result2 = gettyimage_page.filter.video.viewpoint.set_low_angle(1)
            current_result3 = gettyimage_page.filter.video.viewpoint.set_point_view(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.viewpoint.get_tilt()
            check_result_3 = gettyimage_page.filter.video.viewpoint.get_low_angle()
            check_result_4 = gettyimage_page.filter.video.viewpoint.get_point_view()
            case.result = current_result and current_result2 and check_result_1 and check_result_2 and check_result_3 and current_result3 and check_result_4
            gettyimage_page.filter.video.viewpoint.set_tilt(0)
            gettyimage_page.filter.video.viewpoint.set_low_angle(0)
            gettyimage_page.filter.video.viewpoint.set_point_view(0)

        with uuid('8dbfdf48-e563-47d4-bbeb-fb8186628c0d') as case:
            # Image Technique > Real time
            current_result = gettyimage_page.filter.video.image_technique.set_real_time(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.image_technique.get_real_time()
            case.result = current_result and check_result_1 and check_result_2
            gettyimage_page.filter.video.image_technique.set_real_time(0)

        with uuid('74a25c05-f3a0-4628-87ec-cb4e748be019') as case:
            # Image Technique > Time lapse, Slow motion
            current_result = gettyimage_page.filter.video.image_technique.set_time_lapse(1)
            current_result2 = gettyimage_page.filter.video.image_technique.set_slow_motion(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.image_technique.get_time_lapse()
            check_result_3 = gettyimage_page.filter.video.image_technique.get_slow_motion()
            case.result = current_result and current_result2 and check_result_1 and check_result_2 and check_result_3
            gettyimage_page.filter.video.image_technique.set_time_lapse(0)
            gettyimage_page.filter.video.image_technique.set_slow_motion(0)

        with uuid('ce48e893-9843-451e-998b-f703f7be6af5') as case:
            # Image Technique > Black and white, Animation, Selective focus
            current_result = gettyimage_page.filter.video.image_technique.set_black_white(1)
            current_result2 = gettyimage_page.filter.video.image_technique.set_animation(1)
            current_result3 = gettyimage_page.filter.video.image_technique.set_selective_focus(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.image_technique.get_black_white()
            check_result_3 = gettyimage_page.filter.video.image_technique.get_animation()
            check_result_4 = gettyimage_page.filter.video.image_technique.get_selective_focus()
            case.result = current_result and current_result2 and check_result_1 and check_result_2 and check_result_3 and current_result3 and check_result_4
            gettyimage_page.filter.video.image_technique.set_black_white(0)
            gettyimage_page.filter.video.image_technique.set_animation(0)
            gettyimage_page.filter.video.image_technique.set_selective_focus(0)

        with uuid('4abd39b9-3eef-4bbb-b36a-84fa95e014a2') as case:
            # Image Technique > Color
            current_result = gettyimage_page.filter.video.image_technique.set_color(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.image_technique.get_color()
            case.result = current_result and check_result_1 and check_result_2


        with uuid('8cf83712-4860-4e52-be25-b5fbbf285023') as case:
            # Clear all selected filter
            gettyimage_page.click_clear_all_button()
            case.result = not gettyimage_page.filter.video.image_technique.get_color()

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid('cc6d22d1-6f9b-46b1-aa24-3f8e0ea729eb') as case:
            # 2.2. After Search
            # 2.2.1. Search box > input keyword
            # show the string which is user keyin
            media_room_page.import_media_from_shutterstock()
            time.sleep(DELAY_TIME * 8)
            # waiting for shutterstock ready
            gettyimage_page.switch_to_GI()
            gettyimage_page.handle_what_is_stock_media()

            time.sleep(DELAY_TIME * 8)
            download_from_shutterstock_page.search.search_text('go school boy')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)

            search_keyword = download_from_shutterstock_page.search.get_text()
            logger(search_keyword)
            check_result_1 = False if not search_keyword == 'go school boy' else True

            time.sleep(DELAY_TIME * 8)

            case.result = check_result_1

        with uuid('6ad09f3b-2579-423f-8738-3bb093d9992c') as case:
            # 2.2. After Search
            # 2.2.2. Page number > Total Page number
            # show total page number
            time.sleep(20)
            total_page_amount = download_from_shutterstock_page.get_total_page_amount()
            logger(total_page_amount)
            case.result = False if not total_page_amount else True

        with uuid('8b52796d-c37d-4873-9b0e-7208d311d8a5') as case:
            # 2.2. After Search
            # 2.2.1. Search box > input keyword
            # The keyword will be carried to each tab so user does not need to input again
            download_from_shutterstock_page.switch_to_photo()

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'go school boy' else True

            case.result = check_result_1
            time.sleep(2)
            download_from_shutterstock_page.switch_to_video()

        with uuid('cd19e1ed-043e-468d-938d-30c89fd2c753') as case:
            # 2.2. After Search
            # 2.2.2. Page number > Input page number > input box
            # check current page and library panel is updated to user keyin number

            case.result = download_from_shutterstock_page.page_number.set_value('3')

        with uuid('f0358f84-1b36-478f-ae82-1afe7fd08a3c') as case:
            # 2.2. After Search
            # 2.2.2. Page number > Current Page number
            # update current page if click [next/previous] page
            for press_times in range(2):
                download_from_shutterstock_page.click_next_page()
                time.sleep(DELAY_TIME)
            download_from_shutterstock_page.click_previous_page()
            time.sleep(DELAY_TIME)
            current_page_amount = download_from_shutterstock_page.get_page_amount()
            case.result = False if not current_page_amount == 4 else True

            download_from_shutterstock_page.page_number.set_value('1')
            download_from_shutterstock_page.set_scroll_bar(0)
            time.sleep(DELAY_TIME)


        with uuid('4c68796b-eb3b-4ea3-967e-91b622d04604') as case:
            # 2.2. After Search
            # 2.2.3. Library Panel > Icons size / Thumbnail size > [ Extra Large Icons ]
            # Thumbnails show as extra large icons

            case.result = download_from_shutterstock_page.set_library_setting(value='Extra Large')

        with uuid('a5af8d3b-3f4f-40be-853a-c52a3de1e070') as case:
            # 2.2. After Search
            # 2.2.3. Library Panel > Icons size / Thumbnail size > [ Large Icons ]
            # Thumbnails show as large icons

            case.result = download_from_shutterstock_page.set_library_setting(value='Large')

        with uuid('ea00d937-381f-4fc7-ab78-70d907727819') as case:
            # 2.2. After Search
            # 2.2.3. Library Panel > Icons size / Thumbnail size > [ Small Icons ]
            # Thumbnails show as small icons
            case.result = download_from_shutterstock_page.set_library_setting(value='Small')

        with uuid('97b12ec1-7c48-4723-a1d8-1c4b53a908ae') as case:
            # 2.2. After Search
            # 2.2.3. Library Panel > Icons size / Thumbnail size > [ Medium Icons ]
            # Thumbnails show as medium icons
            case.result = download_from_shutterstock_page.set_library_setting(value='Medium')
            time.sleep(DELAY_TIME * 4)
            download_from_shutterstock_page.set_scroll_bar(0)
            time.sleep(DELAY_TIME*3)

        with uuid('be19c61c-8126-4ee0-be6e-9c55fc3cc59f') as case:
            # 2.2. After Search
            # 2.2.4. Select / Deselect > Single select > CheckBox
            # Can select/ deselect single file by ticking the checkbox
            check_result_1 = download_from_shutterstock_page.video.click_thumbnail(4)

            check_result_2 = download_from_shutterstock_page.video.click_thumbnail(4)

            case.result = check_result_1 and check_result_2

        with uuid('d2fc1759-ef88-458c-9255-9378005cb482') as case:
            # 2.2. After Search
            # 2.2.4. Select / Deselect > Single select > thumbnail
            # Can select/ deselect single file by clicking the thumbnail (no "Play" button area)
            check_result_1 = download_from_shutterstock_page.video.click_thumbnail(4)

            check_result_2 = download_from_shutterstock_page.video.click_thumbnail(4)

            case.result = check_result_1 and check_result_2

        with uuid('11421b19-83e5-428f-9b0d-156ab724e0ce') as case:
            # 2.2. After Search
            # 2.2.4. Select / Deselect > Multiple select > CheckBox
            # Can select/ deselect multiple files by ticking the checkbox
            check_result_1 = download_from_shutterstock_page.video.click_thumbnail([0, 4, 2])

            check_result_2 = download_from_shutterstock_page.video.click_thumbnail([0, 4, 2])

            case.result = check_result_1 and check_result_2

        with uuid('66ca0fd0-8ace-473d-bdd7-12ca443cab4f') as case:
            # 2.2. After Search
            # 2.2.8. Selected clip(s)
            # Update the number of the selected clip normally
            case.result = check_result_1

        with uuid('b889070f-fe52-418f-a074-33fbe1ac4c3c') as case:
            # 2.2. After Search
            # 2.2.4. Select / Deselect > Multiple select > thumbnail
            # Can select/ deselect multiple files by clicking the thumbnail (no "Play" button area)
            check_result_1 = download_from_shutterstock_page.video.click_thumbnail(index=0)
            check_result_2 = download_from_shutterstock_page.video.click_thumbnail(index=1)
            check_result_3 = download_from_shutterstock_page.video.click_thumbnail(index=2)
            time.sleep(2)

            check_result_4 = download_from_shutterstock_page.video.click_thumbnail(index=0)
            check_result_5 = download_from_shutterstock_page.video.click_thumbnail(index=1)
            check_result_6 = download_from_shutterstock_page.video.click_thumbnail(index=2)

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4 and check_result_5 \
                and check_result_6

        with uuid('fd6f27c7-2dff-4363-b466-e539e9d0eca8') as case:
            # 2.2. After Search
            # 2.2.7. [ Download ] > Select file
            # Button is enabled
            case.result = check_result_3

        with uuid('b3293380-0eed-457b-92f0-5b352b05a736') as case:
            # 2.2. After Search
            # 2.2.5. Browser Preview > Click the play button > Safari
            # Pop up a window and preview normally in the browser after hover thumbnail and click [play] button
            download_from_shutterstock_page.video.hover_thumbnail(0)
            main_page.mouse.click()
            time.sleep(2)
            case.result = download_from_shutterstock_page.close_pop_up_preview_window()

        with uuid('8778ae61-cd87-4c95-88f1-3e27e6f180e7') as case:
            # 2.2. After Search
            # 2.2.6. Thumbnail > Checkbox
            # Show checkbox normally in upper right corner

            case.result = download_from_shutterstock_page.video.hover_thumbnail(index=0)

        with uuid('f1cb2cd7-d033-477f-ba68-29877f11b8e3') as case:
            # 2.2. After Search
            # 2.2.6. Thumbnail > Highlight
            # Show highlight thumbnail if tick checkbox
            case.result = download_from_shutterstock_page.video.click_thumbnail(3)
            download_from_shutterstock_page.video.click_thumbnail(5)
            download_from_shutterstock_page.video.click_thumbnail(4)
            download_from_shutterstock_page.video.click_thumbnail(2)
            download_from_shutterstock_page.video.click_thumbnail(1)


        with uuid('fb28f1f8-cd1c-475a-b87b-70c1c5cea320') as case:
            # 2.2. After Search
            # 2.2.7. [ Download ] > Progress bar/ Percent
            # Show "Downloading Files[#%]"/ "Remaining Time:" normally
            download_from_shutterstock_page.click_download()
            case.result = main_page.exist(L.download_from_shutterstock.download.btn_cancel)

        with uuid('5ef920f0-585c-4e1b-b5ab-a5f0979daa2c') as case:
            # 2.2. After Search
            # 2.2.7. [ Download ] > [ Cancel ]
            # Cancel downloading
            time.sleep(5)
            check_result_1 = download_from_shutterstock_page.download.click_cancel()

            case.result = check_result_1

        with uuid('6e55e99d-5435-4ef3-81fd-47c7c19a4474') as case:
            # 2.2. After Search
            # 2.2.7. [ Download ] > Complete > Dialog
            # Pop up a dialog "The clips are successfully downloaded and…"
            download_from_shutterstock_page.video.click_thumbnail(5)
            download_from_shutterstock_page.video.click_thumbnail(4)
            download_from_shutterstock_page.video.click_thumbnail(3)
            download_from_shutterstock_page.video.click_thumbnail(2)
            download_from_shutterstock_page.video.click_thumbnail(1)
            download_from_shutterstock_page.video.click_thumbnail(0)
            download_from_shutterstock_page.click_download()
            time.sleep(20)
            download_from_shutterstock_page.download.hd_video.click_no()
            case.result = download_from_shutterstock_page.download.click_complete_ok()
            time.sleep(DELAY_TIME * 20)

        with uuid('17ef8946-5975-43c9-bc4e-9d13ffbe6c64') as case:
            #Switch to Downloaded tab after downloading (free) clips
            image_full_path = Auto_Ground_Truth_Folder + '1_4_1_1.png'
            ground_truth = Ground_Truth_Folder + '1_4_1_1.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.gettyimage.btn_download, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview)


        with uuid('f31d3099-88f1-4bbf-805f-2b3ec473ff31') as case:
            #Downloaded file are available in Downloaded
            case.result = gettyimage_page.hover_heart_icon(0)

        with uuid('f9fd3c0d-e44f-413d-9454-9b4ce8e30b6b') as case:
            #Hide Download button
            case.result = not main_page.exist(L.download_from_shutterstock.btn_download)

        with uuid('266b5443-3a37-4f45-9736-fcb07a7c3bd9') as case:
            #User can click to download again
            gettyimage_page.switch_to_GI()
            gettyimage_page.handle_what_is_stock_media()
            download_from_shutterstock_page.search.search_text('airport child photo')
            time.sleep(2)
            download_from_shutterstock_page.video.click_thumbnail(3)
            download_from_shutterstock_page.click_download()
            for x in range(100):
                if main_page.exist(L.media_room.confirm_dialog.btn_no):
                    media_room_page.handle_high_definition_dialog(option='no')
                    time.sleep(DELAY_TIME*3)
                    break
                else:
                    time.sleep(DELAY_TIME)

            case.result = download_from_shutterstock_page.is_exist(
                {'AXIdentifier': 'IDD_CLALERT', 'AXRoleDescription': 'dialog'}, timeout=10)

            download_from_shutterstock_page.download.click_complete_ok()
            time.sleep(DELAY_TIME * 20)

        with uuid('5224313d-b9a1-4aa6-a309-b98304f55fc9') as case:
            #Show Clear button if there is keyword in search box like Google webpage
            gettyimage_page.switch_to_GI()
            time.sleep(2)
            gettyimage_page.handle_what_is_stock_media()
            download_from_shutterstock_page.search.search_text('apple')
            time.sleep(2)
            case.result = download_from_shutterstock_page.search.click_clear()

        with uuid('49225a7f-2216-4c9c-95a7-bde7c0443cc0') as case:
            # 2.2. After Search
            # 2.2.7. [ Download ] > Complete
            # Downloaded clips are available in the media library

            download_from_shutterstock_page.click_close()

            time.sleep(DELAY_TIME)
            case.result = main_page.select_library_icon_view_media('617790678_fhd')

        with uuid('86d5c1c5-447f-454c-98b9-c977c2e22e2c') as case:
            # Click Download to pop up the purchased message
            media_room_page.enter_media_content()
            media_room_page.import_media_from_shutterstock()
            time.sleep(DELAY_TIME * 8)
            # waiting for shutterstock ready
            gettyimage_page.switch_to_GI()
            time.sleep(2)
            download_from_shutterstock_page.search.search_text('airport')
            time.sleep(DELAY_TIME * 8)
            download_from_shutterstock_page.video.click_thumbnail(6)
            case.result = gettyimage_page.click_add_to_cart_button()

        with uuid('a1221863-0e19-404a-a939-5aadf94afa02') as case:
            # Click Yes to add the unpurchased clips to cart
            case.result = gettyimage_page.click_bubble_cart()

        with uuid('48412cae-e7fd-402e-8fcb-aac3accc8b2b') as case:
            # Click to the checkout flow(4.2 Purchased)

            case.result = gettyimage_page.shopping_cart_click_checkout_button()
            gettyimage_page.handle_checkout_is_complete_dialog('cancel')


        with uuid('9ef8f4f4-0f24-4ddb-9c47-d7e0f2553c6a') as case:
            # 2.2. After Search
            # 2.2.6. Thumbnail > Adjust window size
            # Show the suitable size and thumbnail numbers if adjust window size
            case.result = download_from_shutterstock_page.adjust_window(x=325, y=61, w=949, h=747)

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        #Video > After search
        with uuid('afe43822-08e8-4002-bee0-d463b7dbbec2') as case:
            #Collections > Premium ($)
            media_room_page.import_media_from_shutterstock()
            time.sleep(DELAY_TIME * 8)
            # waiting for shutterstock ready
            gettyimage_page.switch_to_GI()
            gettyimage_page.handle_what_is_stock_media()
            time.sleep(2)
            download_from_shutterstock_page.search.search_text('airport')

            time.sleep(DELAY_TIME * 8)
            gettyimage_page.click_filter_button()
            current_result = gettyimage_page.filter.set_collection_type(2)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_collection_type() == 'Premium ($)' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('ea8f51d7-b71e-4c2d-b99b-a9a8e9c97675') as case:
            # Collections > 365 subscription
            current_result = gettyimage_page.filter.set_collection_type(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_collection_type() == '365 subscription' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('ce59f3c8-d3c7-4d91-8285-d65ff4b3b1c3') as case:
            # Collections > All
            current_result = gettyimage_page.filter.set_collection_type(0)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_collection_type() == 'All' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('9c5cea8d-d23a-41b6-84fe-f3ab2b3e38b6') as case:
            # Sort by > Most popular
            current_result = gettyimage_page.filter.set_sort_by_type(3)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type() == 'Most popular' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('cdcf8706-0cef-406a-adb8-f1b31100bd6a') as case:
            # Sort by > Random
            current_result = gettyimage_page.filter.set_sort_by_type(2)

            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type() == 'Random' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('2b4a6f9b-b3fd-44d4-8c74-15678c0627f4') as case:
            # Sort by > Newest
            current_result = gettyimage_page.filter.set_sort_by_type(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type() == 'Newest' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('f80db502-2673-49d5-8b22-880f44c0d9bd') as case:
            # Sort by > Best matched
            current_result = gettyimage_page.filter.set_sort_by_type(0)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type() == 'Best matched' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('e09e45df-b434-4c06-8a26-a6e4c0dc19b1') as case:
            # Duration > Longer than 1 min  ( Unable to search match media in 20.3630)
            current_result = gettyimage_page.filter.video.set_duration_type(3)
            check_result_2 = True if gettyimage_page.filter.video.get_duration_type() == 'Longer than 1 min' else False
            case.result = current_result and check_result_2 and gettyimage_page.handle_no_match_dialog()

        with uuid('bf505fa4-dfde-4873-8423-e14fa13b2acb') as case:
            # Duration > 1 min or less
            current_result = gettyimage_page.filter.video.set_duration_type(2)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.video.get_duration_type() == '1 min or less' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('18cf56b0-a29a-4798-9d72-65b483302895') as case:
            # Duration > 30s or less
            current_result = gettyimage_page.filter.video.set_duration_type(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.video.get_duration_type() == '30s or less' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('e62f8747-475d-4ced-a4fc-d20992989373') as case:
            # Duration > All
            current_result = gettyimage_page.filter.video.set_duration_type(0)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.video.get_duration_type() == 'All' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('5516db48-dbdd-45a5-b400-d95b0721b581') as case:
            # Resolution (Formats) > SD or above
            gettyimage_page.filter.set_video_scroll_bar(0.6)
            current_result = gettyimage_page.filter.video.set_resolution_type(3)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.video.get_resolution_type() == 'SD or above' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('91c2c9f1-5ae5-44b9-824e-e24a5345941e') as case:
            # Resolution (Formats) > HD or above
            current_result = gettyimage_page.filter.video.set_resolution_type(2)

            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.video.get_resolution_type() == 'HD or above' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('6b4556de-f07b-4938-be09-0e85b8851c3d') as case:
            # Resolution (Formats) > 4K or above
            current_result = gettyimage_page.filter.video.set_resolution_type(1)

            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.video.get_resolution_type() == '4K or above' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('a6b92369-259e-4105-b9f7-385441ff87c3') as case:
            # Resolution (Formats) > All
            current_result = gettyimage_page.filter.video.set_resolution_type(0)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.video.get_resolution_type() == 'All' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('f876ce85-7718-4ec5-98bb-d22cc7657d35') as case:
            # Composition > Close-up
            current_result = gettyimage_page.filter.video.composition.set_close_up(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.composition.get_close_up()
            case.result = current_result and check_result_1 and check_result_2
            gettyimage_page.filter.video.composition.set_close_up(0)

        with uuid('1b090837-cf43-4d37-a3ba-b6e2b04bc732') as case:
            # Composition > Looking at camera, Candid
            current_result = gettyimage_page.filter.video.composition.set_candid(1)
            current_result2 = gettyimage_page.filter.video.composition.set_looking(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.composition.get_candid()
            check_result_3 = gettyimage_page.filter.video.composition.get_looking()
            case.result = current_result and current_result2 and check_result_1 and check_result_2 and check_result_3
            gettyimage_page.filter.video.composition.set_candid(0)
            gettyimage_page.filter.video.composition.set_looking(0)

        with uuid('e8fd1f5c-aeea-48e6-bb9a-e0dd3a302dfe') as case:
            # Viewpoint > Lockdown
            gettyimage_page.filter.set_video_scroll_bar(1)
            current_result = gettyimage_page.filter.video.viewpoint.set_lockdown(1)

            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.viewpoint.get_lockdown()
            case.result = current_result and check_result_1 and check_result_2
            gettyimage_page.filter.video.viewpoint.set_lockdown(0)

        with uuid('74a0371c-ae61-41fe-a4ca-7d9979b5a919') as case:
            # Viewpoint > Panning, Tracking shot ( Unable to search match media in 20.3630)
            gettyimage_page.filter.video.viewpoint.set_panning(1)
            current_result3 = gettyimage_page.handle_no_match_dialog()
            gettyimage_page.filter.video.viewpoint.set_tracking_shot(1)
            current_result2 = gettyimage_page.handle_no_match_dialog()
            current_result = True if gettyimage_page.filter.video.viewpoint.get_panning() and gettyimage_page.filter.video.viewpoint.get_tracking_shot() == 1 else False
            case.result = current_result and current_result2 and current_result3
            gettyimage_page.filter.video.viewpoint.set_panning(0)
            gettyimage_page.handle_no_match_dialog()
            gettyimage_page.filter.video.viewpoint.set_tracking_shot(0)

        with uuid('10632a14-5fd8-4b66-a7ae-f45031e73824') as case:
            # Viewpoint > Aerial view, High angle view
            current_result = gettyimage_page.filter.video.viewpoint.set_aerial_view(1)
            current_result2 = gettyimage_page.filter.video.viewpoint.set_high_angle(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.viewpoint.get_aerial_view()
            check_result_3 = gettyimage_page.filter.video.viewpoint.get_high_angle()
            case.result = current_result and current_result2 and check_result_1 and check_result_2 and check_result_3
            gettyimage_page.filter.video.viewpoint.set_aerial_view(0)
            gettyimage_page.filter.video.viewpoint.set_high_angle(0)

        with uuid('17e5336e-5abb-4852-8d4a-4afbec9b58ab') as case:
            # Viewpoint > Low angle view, Tilt, Point of view
            current_result = gettyimage_page.filter.video.viewpoint.set_tilt(1)
            current_result2 = gettyimage_page.filter.video.viewpoint.set_low_angle(1)
            current_result3 = gettyimage_page.filter.video.viewpoint.set_point_view(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.viewpoint.get_tilt()
            check_result_3 = gettyimage_page.filter.video.viewpoint.get_low_angle()
            check_result_4 = gettyimage_page.filter.video.viewpoint.get_point_view()
            case.result = current_result and current_result2 and check_result_1 and check_result_2 and check_result_3 and current_result3 and check_result_4
            gettyimage_page.filter.video.viewpoint.set_tilt(0)
            gettyimage_page.filter.video.viewpoint.set_low_angle(0)
            gettyimage_page.filter.video.viewpoint.set_point_view(0)

        with uuid('8dbfdf48-e563-47d4-bbeb-fb8186628c0d') as case:
            # Image Technique > Real time
            current_result = gettyimage_page.filter.video.image_technique.set_real_time(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.image_technique.get_real_time()
            case.result = current_result and check_result_1 and check_result_2
            gettyimage_page.filter.video.image_technique.set_real_time(0)

        with uuid('74a25c05-f3a0-4628-87ec-cb4e748be019') as case:
            # Image Technique > Time lapse, Slow motion
            current_result = gettyimage_page.filter.video.image_technique.set_time_lapse(1)
            current_result2 = gettyimage_page.filter.video.image_technique.set_slow_motion(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.image_technique.get_time_lapse()
            check_result_3 = gettyimage_page.filter.video.image_technique.get_slow_motion()
            case.result = current_result and current_result2 and check_result_1 and check_result_2 and check_result_3
            gettyimage_page.filter.video.image_technique.set_time_lapse(0)
            gettyimage_page.filter.video.image_technique.set_slow_motion(0)

        with uuid('ce48e893-9843-451e-998b-f703f7be6af5') as case:
            # Image Technique > Black and white, Animation, Selective focus
            current_result = gettyimage_page.filter.video.image_technique.set_black_white(1)
            current_result2 = gettyimage_page.filter.video.image_technique.set_animation(1)
            current_result3 = gettyimage_page.filter.video.image_technique.set_selective_focus(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.image_technique.get_black_white()
            check_result_3 = gettyimage_page.filter.video.image_technique.get_animation()
            check_result_4 = gettyimage_page.filter.video.image_technique.get_selective_focus()
            case.result = current_result and current_result2 and check_result_1 and check_result_2 and check_result_3 and current_result3 and check_result_4
            gettyimage_page.filter.video.image_technique.set_black_white(0)
            gettyimage_page.filter.video.image_technique.set_animation(0)
            gettyimage_page.filter.video.image_technique.set_selective_focus(0)

        with uuid('4abd39b9-3eef-4bbb-b36a-84fa95e014a2') as case:
            # Image Technique > Color
            current_result = gettyimage_page.filter.video.image_technique.set_color(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.video.image_technique.get_color()
            case.result = current_result and check_result_1 and check_result_2

        with uuid('ac08a0be-3829-4ad4-9c23-130ec7c12128') as case:
            # Clear all selected filter
            gettyimage_page.click_clear_all_button()
            case.result = not gettyimage_page.filter.video.image_technique.get_color()

        with uuid('f53b454d-62e4-4d97-90ab-b5ec6c7313e4') as case:
            # Search nature
            download_from_shutterstock_page.search.click_clear()
            download_from_shutterstock_page.search.search_text('Nature')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'Nature' else True
            check_result_2 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            case.result = check_result_1 and check_result_2


        with uuid('e10ff3e7-af59-426f-8cee-24ca1279e7c0') as case:
            # Search Technology
            download_from_shutterstock_page.search.click_clear()
            download_from_shutterstock_page.search.search_text('Technology')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'Technology' else True
            check_result_2 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            case.result = check_result_1 and check_result_2


        with uuid('26eb45b5-b4f0-4c69-b78d-313405abe726') as case:
            #  Search Football
            download_from_shutterstock_page.search.click_clear()
            download_from_shutterstock_page.search.search_text('Football')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'Football' else True


            check_result_2 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            case.result = check_result_1 and check_result_2


        with uuid('ba973297-d456-44da-99c9-e25143d26ff5') as case:
            # Search Beach
            download_from_shutterstock_page.search.click_clear()
            download_from_shutterstock_page.search.search_text('Beach')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'Beach' else True


            check_result_2 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            case.result = check_result_1 and check_result_2

        with uuid('7ce2281f-9493-4e55-a354-61f4dfcde069') as case:
            # Search Food
            download_from_shutterstock_page.search.click_clear()
            download_from_shutterstock_page.search.search_text('Food')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'Food' else True


            check_result_2 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            case.result = check_result_1 and check_result_2

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_7(self):
        with uuid('fa2ba02b-b700-48a5-9672-b62748254920') as case:
            # 3. Photo
            # 2.1. Before Search
            # 2.1.1. Search box > Default text
            # show "search" / empty in the search box
            media_room_page.import_media_from_shutterstock()
            time.sleep(DELAY_TIME * 8)
            # waiting for shutterstock ready
            gettyimage_page.handle_what_is_stock_media()
            time.sleep(DELAY_TIME * 3)
            download_from_shutterstock_page.switch_to_photo()
            case.result = download_from_shutterstock_page.search.verify_default_string(default='Search')

        with uuid('7afe4a1e-4842-4e69-b755-3f04814514e4') as case:
            # 2.1. Before Search
            # 2.1.1. Search box > Tooltip
            # show "Search"
            case.result = download_from_shutterstock_page.search.verify_tooltip(
                Ground_Truth_Folder + '1_7_1.jpg')

        with uuid('fcd0b2e2-8365-46a6-876a-51a6bd6f8d5a') as case:
            # 2.1. Before Search
            # 2.1.2. Library menu > Default Icons size > [Medium icons]
            # thumbnails show as medium icons. one page has 30 icons
            time.sleep(10)
            download_from_shutterstock_page.set_scroll_bar(1)
            time.sleep(3)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 99})
            #check_result_2 = not main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 30})
            case.result = check_result_1# and check_result_2
            download_from_shutterstock_page.set_scroll_bar(0)
            time.sleep(3)

        with uuid('5544c8ed-6d69-49a5-91a0-c0adbc7a4bb2') as case:
            # 2.1. Before Search
            # 2.1.3. Page number > Current Page number
            # default value is "1"
            current_page_amount = download_from_shutterstock_page.get_page_amount()
            case.result = False if not current_page_amount == 1 else True

        with uuid('aa243d8c-bee4-4984-9d77-96b884eef313') as case:
            # 2.1. Before Search
            # 2.1.3. Page number > Total Page number
            # total page number
            time.sleep(10)
            total_page_amount = download_from_shutterstock_page.get_total_page_amount()
            logger(total_page_amount)
            if total_page_amount >= 31:
                case.result = True
            else:
                case.result = False

        with uuid('5f701a26-4cbe-4c27-95d8-078d27248201') as case:
            # 2.1. Before Search
            # 2.1.4. [Download] > Default status
            # button is disable
            button_status = download_from_shutterstock_page.is_enabled_download()
            case.result = True if not button_status else False

        with uuid('54db8ca6-237f-4ad7-8526-dd107a6ae2ae') as case:
            # 2.1. Before Search
            # 2.1.4. [Download] > Tooltip
            # show "Download"
            case.result = download_from_shutterstock_page.verify_download_tooltip(
                Ground_Truth_Folder + '1_7_2.jpg')

        with uuid('725c3b94-d3f2-4bb4-bb18-88cbed3e7404') as case:
            # 2.1. Before Search
            # 2.1.5. Selected clip(s) > Default value
            # show "0 clips"
            selected_amount = download_from_shutterstock_page.get_selected_amount()
            case.result = False if not selected_amount == 0 else True

        with uuid('25f492c3-fc8c-464e-b0d5-df859f7fa48c') as case:
            #Hover the thumbnail then click the heart icon


            case.result = gettyimage_page.hover_heart_icon(0)
            main_page.left_click()

        with uuid('efcd4d18-c78b-4250-b151-844d5f8f6511') as case:
            #Click to My Favorites tab to browse the added media
            gettyimage_page.click_my_favorites_button()
            case.result = gettyimage_page.click_heart_icon(0)

        with uuid('a61c895b-497e-4c9b-bafd-b028741140c7') as case:
            #Only show bundled stock for the first 6 results
            gettyimage_page.switch_to_GI()
            download_from_shutterstock_page.photo.click_thumbnail(0)
            result0 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(0)
            download_from_shutterstock_page.photo.click_thumbnail(1)
            result1 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(1)
            download_from_shutterstock_page.photo.click_thumbnail(2)
            result2 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(2)
            download_from_shutterstock_page.photo.click_thumbnail(3)
            result3 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(3)
            download_from_shutterstock_page.photo.click_thumbnail(4)
            result4 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(4)
            download_from_shutterstock_page.photo.click_thumbnail(5)
            result5 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(5)
            case.result = result0 and result1 and result2 and result3 and result4 and result5

        with uuid('09ddf341-7e3f-41d2-b31b-093e40b5d565') as case:
            #Show 1/3 premium stock after the first 6 like Pay > Free > Free> Pay > Free > Free> ….
            download_from_shutterstock_page.set_scroll_bar(0.2)
            download_from_shutterstock_page.photo.click_thumbnail(6)
            result0 = gettyimage_page.return_add_to_cart_button_status()
            download_from_shutterstock_page.photo.click_thumbnail(6)
            download_from_shutterstock_page.photo.click_thumbnail(7)
            result1 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(7)
            download_from_shutterstock_page.photo.click_thumbnail(8)
            result2 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(8)
            download_from_shutterstock_page.set_scroll_bar(0.4)
            download_from_shutterstock_page.photo.click_thumbnail(9)
            time.sleep(DELAY_TIME)
            result3 = gettyimage_page.return_add_to_cart_button_status()
            download_from_shutterstock_page.photo.click_thumbnail(9)
            download_from_shutterstock_page.photo.click_thumbnail(10)
            time.sleep(DELAY_TIME)
            result4 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(10)
            download_from_shutterstock_page.photo.click_thumbnail(11)
            result5 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            time.sleep(DELAY_TIME)
            download_from_shutterstock_page.photo.click_thumbnail(11)
            case.result = result0 and result1 and result2 and result3 and result4 and result5

        with uuid('77de2309-eae6-42e5-97e3-9644835539ed') as case:
            #Check the ? items are right
            download_from_shutterstock_page.photo.click_thumbnail(6)
            gettyimage_page.click_add_to_cart_button()
            time.sleep(DELAY_TIME)
            logger(main_page.exist(L.gettyimage.bubble_proceed_to_checkout).AXTitle)
            case.result = True if main_page.exist(L.gettyimage.bubble_proceed_to_checkout).AXTitle == "Proceed to Checkout\n(1 item(s))" else False

        with uuid('1fcf2819-5640-4b81-b9c0-444b5650baf3') as case:
            #Show the message "Added to cart" for 3 sec
            current_result = main_page.is_exist(L.gettyimage.bubble_cart)
            time.sleep(4)
            current_result2 = main_page.is_not_exist(L.gettyimage.bubble_cart)
            case.result = current_result and current_result2

        with uuid('abb744fe-fcfe-45b9-bd13-93b344909254') as case:
            #PC: Click to open browser to AK’s page and pop up waiting dialog
            gettyimage_page.click_add_to_cart_button()
            time.sleep(1)
            case.result = gettyimage_page.click_bubble_proceed_checkout()
            gettyimage_page.handle_checkout_is_complete_dialog('cancel')

        with uuid('34522dcd-33fa-4e4c-9cc6-14d8d660c06b') as case:
            #Download a free media and add a pay media to cart
            time.sleep(2)
            download_from_shutterstock_page.photo.click_thumbnail(6)
            download_from_shutterstock_page.photo.click_thumbnail(7)
            current_result2 = download_from_shutterstock_page.click_download()
            time.sleep(10)
            download_from_shutterstock_page.download.click_complete_ok()
            time.sleep(10)
            current_result = gettyimage_page.click_shopping_cart_button()
            case.result = current_result and current_result2

        with uuid('7947b161-5728-4034-a9f3-729cde78116c') as case:
            #"Added to cart" message > Pop up shopping cart dialog
            time.sleep(2)
            case.result = gettyimage_page.is_enter_shopping_cart_window()

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_8(self):
        with uuid('92e47bc1-9dbe-4703-8ea1-41f444191000') as case:
            #Photo > Before Search
            #Collections > Premium ($)
            media_room_page.import_media_from_shutterstock()
            time.sleep(DELAY_TIME * 8)
            # waiting for shutterstock ready
            gettyimage_page.switch_to_GI()
            gettyimage_page.handle_what_is_stock_media()

            time.sleep(DELAY_TIME * 8)
            download_from_shutterstock_page.switch_to_photo()
            time.sleep(DELAY_TIME * 8)
            gettyimage_page.click_filter_button()
            current_result = gettyimage_page.filter.set_collection_type(5)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_collection_type(set_video=0) == 'Premium ($)' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('530f15bd-2d02-42ee-a953-e4ec8c4be6a1') as case:
            # Collections > 365 subscription
            current_result = gettyimage_page.filter.set_collection_type(4)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_collection_type(set_video=0) == '365 subscription' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('4c808aac-64fe-46c6-81e2-a52812fcf061') as case:
            # Collections > All
            current_result = gettyimage_page.filter.set_collection_type(3)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_collection_type(set_video=0) == 'All' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('3525951e-a26b-46fa-93ec-312d3721bec9') as case:
            # Sort by > Most popular
            current_result = gettyimage_page.filter.set_sort_by_type(7)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type(set_video=0) == 'Most popular' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('8e98ef78-76c9-403c-b57d-21ae3c697976') as case:
            # Sort by > Random
            current_result = gettyimage_page.filter.set_sort_by_type(6)

            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type(set_video=0) == 'Random' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('dccc1457-8993-4a2f-b52e-87d9a3ff3bc1') as case:
            # Sort by > Newest
            current_result = gettyimage_page.filter.set_sort_by_type(5)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type(set_video=0) == 'Newest' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('c02ec632-97cd-419d-983a-1f067d348cf6') as case:
            # Sort by > Best matched
            current_result = gettyimage_page.filter.set_sort_by_type(4)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type(set_video=0) == 'Best matched' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('24d86708-282c-4ce3-bdf9-998df772bc08') as case:
            # Orientation > Vertical
            current_result = gettyimage_page.filter.photo.orientation.set_vertical(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.orientation.get_vertical()
            case.result = current_result and check_result_1 and check_result_2
            gettyimage_page.filter.photo.orientation.set_vertical(0)

        with uuid('c9bfd5a5-6c28-4a0a-87d9-c94a4adc5d92') as case:
            # Orientation > Horizontal, Square, Panoramic Horizontal
            current_result = gettyimage_page.filter.photo.orientation.set_horizontal(1)
            current_result1 = gettyimage_page.filter.photo.orientation.set_square(1)
            current_result2 = gettyimage_page.filter.photo.orientation.set_panoramic(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.orientation.get_horizontal()
            check_result_3 = gettyimage_page.filter.photo.orientation.get_square()
            check_result_4 = gettyimage_page.filter.photo.orientation.get_panoramic()
            case.result = current_result and current_result1 and current_result2 and check_result_1 and check_result_2 and check_result_3 and check_result_4
            gettyimage_page.filter.photo.orientation.set_horizontal(0)
            gettyimage_page.filter.photo.orientation.set_square(0)
            gettyimage_page.filter.photo.orientation.set_panoramic(0)

        with uuid('73d3df58-1918-42ee-b5bf-8aa1f2abe3aa') as case:
            # Image Style > Abstract
            time.sleep(2)
            gettyimage_page.filter.set_photo_scroll_bar(1)
            current_result = gettyimage_page.filter.photo.image_style.set_abstract(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.image_style.get_abstract()
            case.result = current_result and check_result_1 and check_result_2
            gettyimage_page.filter.photo.image_style.set_abstract(0)


        with uuid('2cce86a1-a2d7-48af-9059-9aa049358ed5') as case:
            # Image Style > Portrait, Close-up
            current_result = gettyimage_page.filter.photo.image_style.set_portrait(1)
            current_result1 = gettyimage_page.filter.photo.image_style.set_close_up(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.image_style.get_portrait()
            check_result_3 = gettyimage_page.filter.photo.image_style.get_close_up()
            case.result = current_result and current_result1 and check_result_1 and check_result_2 and check_result_3
            gettyimage_page.filter.photo.image_style.set_portrait(0)
            gettyimage_page.filter.photo.image_style.set_close_up(0)

        with uuid('c913e524-2e1d-4c2d-986e-50d64da6313f') as case:
            # Image Style > Sparse, Cut out ,Full frame
            current_result = gettyimage_page.filter.photo.image_style.set_sparse(1)
            current_result1 = gettyimage_page.filter.photo.image_style.set_cut_out(1)
            current_result2 = gettyimage_page.filter.photo.image_style.set_full_frame(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.image_style.get_sparse()
            check_result_3 = gettyimage_page.filter.photo.image_style.get_cut_out()
            check_result_4 = gettyimage_page.filter.photo.image_style.get_full_frame()
            case.result = current_result and current_result1 and check_result_1 and check_result_2 and check_result_3 and check_result_4 and current_result2
            gettyimage_page.filter.photo.image_style.set_sparse(0)
            gettyimage_page.filter.photo.image_style.set_cut_out(0)
            gettyimage_page.filter.photo.image_style.set_full_frame(0)

        with uuid('2067ebcf-7b67-4b02-9158-0dfa552fcc5f') as case:
            # Image Style > Copy space, Macro, Still life
            current_result = gettyimage_page.filter.photo.image_style.set_copy_space(1)
            current_result1 = gettyimage_page.filter.photo.image_style.set_macro(1)
            current_result2 = gettyimage_page.filter.photo.image_style.set_still_life(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.image_style.get_copy_space()
            check_result_3 = gettyimage_page.filter.photo.image_style.get_macro()
            check_result_4 = gettyimage_page.filter.photo.image_style.get_still_life()
            case.result = current_result and current_result1 and check_result_1 and check_result_2 and check_result_3 and check_result_4 and current_result2
            gettyimage_page.filter.photo.image_style.set_copy_space(0)
            gettyimage_page.filter.photo.image_style.set_macro(0)
            gettyimage_page.filter.photo.image_style.set_still_life(0)

        with uuid('44e09b04-fd69-40b0-b4e1-64b133c67332') as case:
            # Number of People > No people
            current_result = gettyimage_page.filter.photo.number_people.set_no(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.number_people.get_no()
            case.result = current_result and current_result1 and check_result_1 and check_result_2
            gettyimage_page.filter.photo.number_people.set_no(0)


        with uuid('5252de83-d20a-40f9-886b-a4e2e8821006') as case:
            # Number of People > One person, Two people
            current_result = gettyimage_page.filter.photo.number_people.set_one(1)
            current_result1 = gettyimage_page.filter.photo.number_people.set_two(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.number_people.get_one()
            check_result_3 = gettyimage_page.filter.photo.number_people.get_two()
            case.result = current_result and current_result1 and check_result_1 and check_result_2 and check_result_3
            gettyimage_page.filter.photo.number_people.set_one(0)
            gettyimage_page.filter.photo.number_people.set_two(0)

        with uuid('6ef967e3-db35-450d-8419-c652b340eca4') as case:
            # Number of People > Group of people
            current_result = gettyimage_page.filter.photo.number_people.set_group(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.number_people.get_group()
            case.result = current_result and current_result1 and check_result_1 and check_result_2

        with uuid('641b9b4b-b852-427f-bda4-634a2a320dd0') as case:
            # Clear all selected filter
            gettyimage_page.click_clear_all_button()
            case.result = not gettyimage_page.filter.photo.number_people.get_group()
        download_from_shutterstock_page.click_close()

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_9(self):
        with uuid('a7d07281-7097-4b31-97f8-9fb0e94af6c8') as case:
            # Photo
            # 2.2. After Search
            # 2.2.1. Search box > input keyword
            # show the string which is user keyin
            media_room_page.import_media_from_shutterstock()
            time.sleep(DELAY_TIME * 8)
            # waiting for shutterstock ready
            gettyimage_page.switch_to_GI()
            gettyimage_page.handle_what_is_stock_media()

            time.sleep(DELAY_TIME * 8)
            download_from_shutterstock_page.switch_to_photo()
            time.sleep(DELAY_TIME * 8)
            download_from_shutterstock_page.search.search_text('airport')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'airport' else True

            time.sleep(DELAY_TIME * 8)

            case.result = check_result_1

        with uuid('a13d37d1-33ac-4046-9da7-6463e36a735b') as case:
            # 2.2. After Search
            # 2.2.2. Page number > Total Page number
            # show total page number
            time.sleep(10)
            total_page_amount = download_from_shutterstock_page.get_total_page_amount()
            logger(total_page_amount)
            case.result = False if not total_page_amount == 40 else True

        with uuid('beef8666-7f32-4bf6-9af6-1a4b46d6faa4') as case:
            # 2.2. After Search
            # 2.2.1. Search box > input keyword
            # The keyword will be carried to each tab so user does not need to input again
            download_from_shutterstock_page.switch_to_video()

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'airport' else True

            case.result = check_result_1
            time.sleep(2)
            download_from_shutterstock_page.switch_to_photo()

        with uuid('21851464-873b-4c23-9e13-563a7b459540') as case:
            # 2.2. After Search
            # 2.2.2. Page number > Input page number > input box
            # check current page and library panel is updated to user keyin number

            case.result = download_from_shutterstock_page.page_number.set_value('3')

        with uuid('70480bad-f342-4ca5-9e09-201462912ba2') as case:
            # 2.2. After Search
            # 2.2.2. Page number > Current Page number
            # update current page if click [next/previous] page
            for press_times in range(2):
                download_from_shutterstock_page.click_next_page()
                time.sleep(DELAY_TIME)
            download_from_shutterstock_page.click_previous_page()
            time.sleep(DELAY_TIME)
            current_page_amount = download_from_shutterstock_page.get_page_amount()
            case.result = False if not current_page_amount == 4 else True

            download_from_shutterstock_page.page_number.set_value('1')



        with uuid('fa2943fb-5036-4d2d-a4dd-f7002772fabe') as case:
            # 2.2. After Search
            # 2.2.3. Library Panel > Icons size / Thumbnail size > [ Extra Large Icons ]
            # Thumbnails show as extra large icons

            case.result = download_from_shutterstock_page.set_library_setting(value='Extra Large')

        with uuid('355b6df0-85c2-4b59-9093-546d744647ec') as case:
            # 2.2. After Search
            # 2.2.3. Library Panel > Icons size / Thumbnail size > [ Large Icons ]
            # Thumbnails show as large icons

            case.result = download_from_shutterstock_page.set_library_setting(value='Large')

        with uuid('80eafdf3-05fd-4954-bf4a-18bd70675b05') as case:
            # 2.2. After Search
            # 2.2.3. Library Panel > Icons size / Thumbnail size > [ Small Icons ]
            # Thumbnails show as small icons
            case.result = download_from_shutterstock_page.set_library_setting(value='Small')

        with uuid('8b19f2a3-0b8b-4b81-a83f-aed82bf70e9c') as case:
            # 2.2. After Search
            # 2.2.3. Library Panel > Icons size / Thumbnail size > [ Medium Icons ]
            # Thumbnails show as medium icons
            case.result = download_from_shutterstock_page.set_library_setting(value='Medium')
            time.sleep(2)

        with uuid('6c8e09a8-d297-4264-b741-4ff895068a6e') as case:
            # 2.2. After Search
            # 2.2.4. Select / Deselect > Single select > CheckBox
            # Can select/ deselect single file by ticking the checkbox
            check_result_1 = download_from_shutterstock_page.video.click_thumbnail(4)

            check_result_2 = download_from_shutterstock_page.video.click_thumbnail(4)

            case.result = check_result_1 and check_result_2

        with uuid('498e3534-ea17-49f1-9ca1-d71e80c8ff60') as case:
            # 2.2. After Search
            # 2.2.4. Select / Deselect > Single select > thumbnail
            # Can select/ deselect single file by clicking the thumbnail (no "Play" button area)
            check_result_1 = download_from_shutterstock_page.video.click_thumbnail(4)

            check_result_2 = download_from_shutterstock_page.video.click_thumbnail(4)

            case.result = check_result_1 and check_result_2

        with uuid('73a65c8a-f666-487d-90be-6068f4a03a81') as case:
            # 2.2. After Search
            # 2.2.4. Select / Deselect > Multiple select > CheckBox
            # Can select/ deselect multiple files by ticking the checkbox
            check_result_1 = download_from_shutterstock_page.video.click_thumbnail([0, 4, 2])

            check_result_2 = download_from_shutterstock_page.video.click_thumbnail([0, 4, 2])

            case.result = check_result_1 and check_result_2

        with uuid('b4153b84-4d9f-4c01-a66f-47864b4e3bf6') as case:
            # 2.2. After Search
            # 2.2.8. Selected clip(s)
            # Update the number of the selected clip normally
            case.result = check_result_1

        with uuid('75f9c8e9-89ca-4f08-a30e-8e1468617d29') as case:
            # 2.2. After Search
            # 2.2.4. Select / Deselect > Multiple select > thumbnail
            # Can select/ deselect multiple files by clicking the thumbnail (no "Play" button area)
            check_result_1 = download_from_shutterstock_page.video.click_thumbnail(index=0)
            check_result_2 = download_from_shutterstock_page.video.click_thumbnail(index=1)
            check_result_3 = download_from_shutterstock_page.video.click_thumbnail(index=2)
            time.sleep(2)

            check_result_4 = download_from_shutterstock_page.video.click_thumbnail(index=0)
            check_result_5 = download_from_shutterstock_page.video.click_thumbnail(index=1)
            check_result_6 = download_from_shutterstock_page.video.click_thumbnail(index=2)

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4 and check_result_5 \
                and check_result_6

        with uuid('ffda65aa-514b-43a8-9ca4-f28bd8a749e9') as case:
            # 2.2. After Search
            # 2.2.7. [ Download ] > Select file
            # Button is enabled
            case.result = check_result_3

        with uuid('589f61b9-13c7-4d11-9195-12897e9e70ee') as case:
            # 2.2. After Search
            # 2.2.5. Browser Preview > Click the play button > Safari
            # Pop up a window and preview normally in the browser after hover thumbnail and click [play] button
            download_from_shutterstock_page.video.hover_thumbnail(0)
            main_page.mouse.click()
            time.sleep(2)
            case.result = download_from_shutterstock_page.close_pop_up_preview_window()

        with uuid('01d8bf0f-90c8-4e03-aa47-c68ae670aac2') as case:
            # 2.2. After Search
            # 2.2.6. Thumbnail > Checkbox
            # Show checkbox normally in upper right corner
            case.result = download_from_shutterstock_page.video.hover_thumbnail(index=0)

        with uuid('c4152889-15bd-4952-a88a-79ed0313bcf2') as case:
            # 2.2. After Search
            # 2.2.6. Thumbnail > Highlight
            # Show highlight thumbnail if tick checkbox
            case.result = download_from_shutterstock_page.video.click_thumbnail(4)
            download_from_shutterstock_page.video.click_thumbnail(index=0)
            download_from_shutterstock_page.video.click_thumbnail(index=1)
            download_from_shutterstock_page.video.click_thumbnail(index=2)


        with uuid('a669c477-94cc-4d65-99ba-3516edf91c1d') as case:
            # 2.2. After Search
            # 2.2.7. [ Download ] > Progress bar/ Percent
            # Show "Downloading Files[#%]"/ "Remaining Time:" normally
            download_from_shutterstock_page.click_download()
            case.result = download_from_shutterstock_page.download.verify_progress()

        with uuid('b499378b-c09e-4174-ae37-476c3eb39c4e') as case:
            # 2.2. After Search
            # 2.2.7. [ Download ] > [ Cancel ]
            # Cancel downloading
            check_result_1 = download_from_shutterstock_page.download.click_cancel()

            case.result = check_result_1

        with uuid('f67cebae-662e-4508-95be-b7fb1068e8a5') as case:
            # 2.2. After Search
            # 2.2.7. [ Download ] > Complete > Dialog
            # Pop up a dialog "The clips are successfully downloaded and…"
            download_from_shutterstock_page.video.click_thumbnail(index=0)
            download_from_shutterstock_page.video.click_thumbnail(index=1)
            download_from_shutterstock_page.video.click_thumbnail(index=2)
            download_from_shutterstock_page.click_download()
            case.result = download_from_shutterstock_page.is_exist(
                {'AXIdentifier': 'IDD_CLALERT', 'AXRoleDescription': 'dialog'}, timeout=10)

            download_from_shutterstock_page.download.click_complete_ok()
            time.sleep(DELAY_TIME * 10)

        with uuid('71f38ab2-98f3-4582-8bc1-4ecfdbaf6dcb') as case:
            #Switch to Downloaded tab after downloading (free) clips
            image_full_path = Auto_Ground_Truth_Folder + '1_9_2.png'
            ground_truth = Ground_Truth_Folder + '1_9_2.png'
            current_preview = download_from_shutterstock_page.snapshot(
                locator=L.gettyimage.btn_download, file_name=image_full_path)
            case.result = download_from_shutterstock_page.compare(ground_truth, current_preview)


        with uuid('b07606fb-1068-45cc-ac6e-f837e2050a8e') as case:
            #Downloaded file are available in Downloaded
            case.result = gettyimage_page.hover_heart_icon(0)

        with uuid('0c8453d0-53e7-4156-83ac-fefa0c5f731d') as case:
            #Hide Download button
            case.result = not main_page.exist(L.download_from_shutterstock.btn_download)

        with uuid('1ee58d57-10bd-4677-9950-43ff9f21da65') as case:
            #User can click to download again
            gettyimage_page.switch_to_GI()
            gettyimage_page.handle_what_is_stock_media()
            download_from_shutterstock_page.switch_to_photo()
            download_from_shutterstock_page.search.search_text('airport')
            time.sleep(2)
            download_from_shutterstock_page.video.click_thumbnail(4)
            download_from_shutterstock_page.click_download()
            case.result = download_from_shutterstock_page.is_exist(
                {'AXIdentifier': 'IDD_CLALERT', 'AXRoleDescription': 'dialog'}, timeout=10)

            download_from_shutterstock_page.download.click_complete_ok()
            time.sleep(DELAY_TIME * 10)

        with uuid('85fc1055-2d92-4ba2-910f-349ff66bcd86') as case:
            #Show Clear button if there is keyword in search box like Google webpage
            case.result = download_from_shutterstock_page.search.click_clear

        with uuid('b07606fb-1068-45cc-ac6e-f837e2050a8e') as case:
            # 2.2. After Search
            # 2.2.7. [ Download ] > Complete
            # Downloaded clips are available in the media library

            download_from_shutterstock_page.click_close()
            time.sleep(DELAY_TIME*2)
            img_before = main_page.snapshot(locator=L.base.Area.preview.main)
            time.sleep(DELAY_TIME)
            media_room_page.media_filter_display_video_only()
            time.sleep(DELAY_TIME)
            img_after = main_page.snapshot(locator=L.base.Area.preview.main)
            check_result = main_page.compare(img_before, img_after, similarity=0.99)
            logger(check_result)
            case.result = not check_result
            media_room_page.media_filter_display_all()
    
        with uuid('a0f4eb41-5d73-41c4-8fd2-9eec4655abd0') as case:
            # Click Download to pop up the purchased message
            media_room_page.enter_media_content()
            media_room_page.import_media_from_shutterstock()
            time.sleep(DELAY_TIME * 8)
            # waiting for shutterstock ready
            gettyimage_page.switch_to_GI()
            time.sleep(2)
            download_from_shutterstock_page.switch_to_photo()
            time.sleep(DELAY_TIME * 8)
            download_from_shutterstock_page.search.search_text('airport')
            time.sleep(DELAY_TIME * 8)
            download_from_shutterstock_page.video.click_thumbnail(6)
            case.result = gettyimage_page.click_add_to_cart_button()

        with uuid('cddb63c6-e4fc-4792-aa1d-63065a42e67e') as case:
            # Click Yes to add the unpurchased clips to cart
            case.result = gettyimage_page.click_bubble_cart()

        with uuid('e1b77674-c085-44a6-861b-6d760caff431') as case:
            # Click to the checkout flow(4.2 Purchased)
            case.result = gettyimage_page.shopping_cart_click_checkout_button()
            gettyimage_page.handle_checkout_is_complete_dialog('cancel')


        with uuid('d68a6caa-cf20-426a-bdb6-bc9a1cc96a85') as case:
            # 2.2. After Search
            # 2.2.6. Thumbnail > Adjust window size
            # Show the suitable size and thumbnail numbers if adjust window size
            case.result = download_from_shutterstock_page.adjust_window(x=325, y=61, w=949, h=747)

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_10(self):
        #Photo > After search
        with uuid('25fd81b7-e84b-4516-9c24-db9fb70adba3') as case:
            #Hover the thumbnail then click the heart icon
            media_room_page.import_media_from_shutterstock()
            time.sleep(DELAY_TIME * 8)
            # waiting for shutterstock ready
            gettyimage_page.switch_to_GI()
            gettyimage_page.handle_what_is_stock_media()

            time.sleep(DELAY_TIME * 8)
            download_from_shutterstock_page.switch_to_photo()
            time.sleep(DELAY_TIME * 8)
            download_from_shutterstock_page.search.search_text('airport')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)

            case.result = gettyimage_page.hover_heart_icon(1)
            main_page.left_click()


        with uuid('1315e7d3-5c96-4f61-91fc-ca6dd027c63c') as case:
            #Click to My Favorites tab to browse the added media
            gettyimage_page.click_my_favorites_button()
            case.result = gettyimage_page.click_heart_icon(0)

        with uuid('a42dedae-9774-4852-9c19-2215c1c4df61') as case:
            #Only show bundled stock for the first 6 results
            gettyimage_page.switch_to_GI()
            download_from_shutterstock_page.search.search_text('airport')
            download_from_shutterstock_page.photo.click_thumbnail(0)
            result0 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(0)
            download_from_shutterstock_page.photo.click_thumbnail(1)
            result1 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(1)
            download_from_shutterstock_page.photo.click_thumbnail(2)
            result2 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(2)
            download_from_shutterstock_page.photo.click_thumbnail(3)
            result3 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(3)
            download_from_shutterstock_page.photo.click_thumbnail(4)
            result4 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(4)
            download_from_shutterstock_page.photo.click_thumbnail(5)
            result5 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(5)
            case.result = result0 and result1 and result2 and result3 and result4 and result5

        with uuid('2916a701-d576-4a7e-bac6-95e3ad43c438') as case:
            #Show 1/3 premium stock after the first 6 like Pay > Free > Free> Pay > Free > Free> ….
            download_from_shutterstock_page.set_scroll_bar(0.2)
            time.sleep(2)
            download_from_shutterstock_page.photo.click_thumbnail(6)
            result0 = gettyimage_page.return_add_to_cart_button_status()
            time.sleep(2)
            download_from_shutterstock_page.photo.click_thumbnail(6)
            download_from_shutterstock_page.photo.click_thumbnail(7)
            result1 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(7)
            download_from_shutterstock_page.photo.click_thumbnail(8)
            result2 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(8)
            download_from_shutterstock_page.photo.click_thumbnail(9)
            result3 = gettyimage_page.return_add_to_cart_button_status()
            download_from_shutterstock_page.photo.click_thumbnail(9)
            download_from_shutterstock_page.photo.click_thumbnail(10)
            result4 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(10)
            download_from_shutterstock_page.photo.click_thumbnail(11)
            result5 = main_page.is_exist(L.download_from_shutterstock.btn_download)
            download_from_shutterstock_page.photo.click_thumbnail(11)
            case.result = result0 and result1 and result2 and result3 and result4 and result5

        with uuid('c55ebcae-6fb9-42dc-a389-0abf76375d8f') as case:
            #Check the ? items are right
            download_from_shutterstock_page.photo.click_thumbnail(6)
            gettyimage_page.click_add_to_cart_button()
            case.result = True if main_page.exist(L.gettyimage.bubble_proceed_to_checkout).AXTitle == "Proceed to Checkout\n(1 item(s))" else False

        with uuid('cb365da7-b37d-4c1b-9dfe-e4e26f98652b') as case:
            #Show the message "Added to cart" for 3 sec
            current_result = main_page.is_exist(L.gettyimage.bubble_cart)
            time.sleep(4)
            current_result2 = main_page.is_not_exist(L.gettyimage.bubble_cart)
            case.result = current_result and current_result2

        with uuid('f8d8e23b-2046-4189-aac0-371c74c5fcc8') as case:
            #PC: Click to open browser to AK’s page and pop up waiting dialog
            gettyimage_page.click_add_to_cart_button()
            case.result = gettyimage_page.click_bubble_proceed_checkout()
            time.sleep(6)
            gettyimage_page.handle_checkout_is_complete_dialog('cancel')
            time.sleep(2)

        with uuid('efcf1e70-278e-4e41-b910-766d37352d87') as case:

            # Download a free media and add a pay media to cart
            time.sleep(DELAY_TIME*2)
            download_from_shutterstock_page.photo.click_thumbnail(6)
            download_from_shutterstock_page.photo.click_thumbnail(7)
            current_result2 = download_from_shutterstock_page.click_download()
            time.sleep(10)
            download_from_shutterstock_page.download.hd_video.click_no()
            time.sleep(2)
            download_from_shutterstock_page.download.click_complete_ok()
            time.sleep(15)
            current_result = gettyimage_page.click_shopping_cart_button()
            case.result = current_result and current_result2

        with uuid('849cc450-a3b1-412e-b430-75a089f1810f') as case:
            # "Added to cart" message > Pop up shopping cart dialog
            time.sleep(2)
            case.result = gettyimage_page.is_enter_shopping_cart_window()

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_11(self):
        with uuid('28c7032f-f321-4de8-9644-33eb7a43f38c') as case:
            #Photo > After Search
            #Collections > Premium ($)
            media_room_page.import_media_from_shutterstock()
            time.sleep(DELAY_TIME * 8)
            # waiting for shutterstock ready
            gettyimage_page.switch_to_GI()
            gettyimage_page.handle_what_is_stock_media()

            time.sleep(DELAY_TIME * 8)
            download_from_shutterstock_page.switch_to_photo()
            download_from_shutterstock_page.search.search_text('airport')
            time.sleep(DELAY_TIME * 8)
            gettyimage_page.click_filter_button()
            current_result = gettyimage_page.filter.set_collection_type(5)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_collection_type(set_video=0) == 'Premium ($)' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('cd37e1c8-647a-45c5-89fa-072a185137cb') as case:
            # Collections > 365 subscription
            current_result = gettyimage_page.filter.set_collection_type(4)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_collection_type(set_video=0) == '365 subscription' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('079b22ee-fcc8-4d14-a701-dcd86a65ebb4') as case:
            # Collections > All
            current_result = gettyimage_page.filter.set_collection_type(3)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_collection_type(set_video=0) == 'All' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('5e0ef090-e26a-4e62-8197-8cf8c5e8637d') as case:
            # Sort by > Most popular
            current_result = gettyimage_page.filter.set_sort_by_type(7)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type(set_video=0) == 'Most popular' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('7854feaf-9708-433c-81a5-162214b59e46') as case:
            # Sort by > Random
            current_result = gettyimage_page.filter.set_sort_by_type(6)

            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type(set_video=0) == 'Random' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('739c172d-e5f7-48b9-b0db-48e704b6dc71') as case:
            # Sort by > Newest
            current_result = gettyimage_page.filter.set_sort_by_type(5)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type(set_video=0) == 'Newest' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('2b4d330a-2684-413d-a2b6-5d4739cd8b8e') as case:
            # Sort by > Best matched
            current_result = gettyimage_page.filter.set_sort_by_type(4)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = True if gettyimage_page.filter.get_sort_by_type(set_video=0) == 'Best matched' else False
            case.result = current_result and check_result_1 and check_result_2

        with uuid('76577936-f366-4e63-b158-2147fef2df42') as case:
            # Orientation > Vertical
            current_result = gettyimage_page.filter.photo.orientation.set_vertical(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.orientation.get_vertical()
            case.result = current_result and check_result_1 and check_result_2
            gettyimage_page.filter.photo.orientation.set_vertical(0)

        with uuid('c5278ef5-3056-43f0-9051-ea58f8c9053e') as case:
            # Orientation > Horizontal, Square, Panoramic Horizontal
            current_result = gettyimage_page.filter.photo.orientation.set_horizontal(1)
            current_result1 = gettyimage_page.filter.photo.orientation.set_square(1)
            current_result2 = gettyimage_page.filter.photo.orientation.set_panoramic(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.orientation.get_horizontal()
            check_result_3 = gettyimage_page.filter.photo.orientation.get_square()
            check_result_4 = gettyimage_page.filter.photo.orientation.get_panoramic()
            case.result = current_result and current_result1 and current_result2 and check_result_1 and check_result_2 and check_result_3 and check_result_4
            gettyimage_page.filter.photo.orientation.set_horizontal(0)
            gettyimage_page.filter.photo.orientation.set_square(0)
            gettyimage_page.filter.photo.orientation.set_panoramic(0)

        with uuid('5817611a-776e-4873-874f-f935fe1dc442') as case:
            # Image Style > Abstract
            time.sleep(2)
            gettyimage_page.filter.set_photo_scroll_bar(1)
            current_result = gettyimage_page.filter.photo.image_style.set_abstract(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.image_style.get_abstract()
            case.result = current_result and check_result_1 and check_result_2
            gettyimage_page.filter.photo.image_style.set_abstract(0)


        with uuid('9bcc4825-c149-4f77-8b7c-05b9aa988383') as case:
            # Image Style > Portrait, Close-up
            current_result = gettyimage_page.filter.photo.image_style.set_portrait(1)
            current_result1 = gettyimage_page.filter.photo.image_style.set_close_up(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.image_style.get_portrait()
            check_result_3 = gettyimage_page.filter.photo.image_style.get_close_up()
            case.result = current_result and current_result1 and check_result_1 and check_result_2 and check_result_3
            gettyimage_page.filter.photo.image_style.set_portrait(0)
            gettyimage_page.filter.photo.image_style.set_close_up(0)

        with uuid('1d8e0afe-11fb-4e5f-a85e-cd041aca3a86') as case:
            # Image Style > Sparse, Cut out ,Full frame
            current_result = gettyimage_page.filter.photo.image_style.set_sparse(1)
            current_result1 = gettyimage_page.filter.photo.image_style.set_cut_out(1)
            current_result2 = gettyimage_page.filter.photo.image_style.set_full_frame(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.image_style.get_sparse()
            check_result_3 = gettyimage_page.filter.photo.image_style.get_cut_out()
            check_result_4 = gettyimage_page.filter.photo.image_style.get_full_frame()
            case.result = current_result and current_result1 and check_result_1 and check_result_2 and check_result_3 and check_result_4 and current_result2
            gettyimage_page.filter.photo.image_style.set_sparse(0)
            gettyimage_page.filter.photo.image_style.set_cut_out(0)
            gettyimage_page.filter.photo.image_style.set_full_frame(0)

        with uuid('b27bb45c-46d5-4ae5-bb9c-1d5779df00e4') as case:
            # Image Style > Copy space, Macro, Still life
            current_result = gettyimage_page.filter.photo.image_style.set_copy_space(1)
            current_result1 = gettyimage_page.filter.photo.image_style.set_macro(1)
            current_result2 = gettyimage_page.filter.photo.image_style.set_still_life(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.image_style.get_copy_space()
            check_result_3 = gettyimage_page.filter.photo.image_style.get_macro()
            check_result_4 = gettyimage_page.filter.photo.image_style.get_still_life()
            case.result = current_result and current_result1 and check_result_1 and check_result_2 and check_result_3 and check_result_4 and current_result2
            gettyimage_page.filter.photo.image_style.set_copy_space(0)
            gettyimage_page.filter.photo.image_style.set_macro(0)
            gettyimage_page.filter.photo.image_style.set_still_life(0)

        with uuid('8ee1918d-6268-463c-85e6-d4c76eeca301') as case:
            # Number of People > No people
            current_result = gettyimage_page.filter.photo.number_people.set_no(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.number_people.get_no()
            case.result = current_result and current_result1 and check_result_1 and check_result_2
            gettyimage_page.filter.photo.number_people.set_no(0)


        with uuid('1854a8c8-ae70-4e11-9867-07e4b6ec459a') as case:
            # Number of People > One person, Two people
            current_result = gettyimage_page.filter.photo.number_people.set_one(1)
            current_result1 = gettyimage_page.filter.photo.number_people.set_two(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.number_people.get_one()
            check_result_3 = gettyimage_page.filter.photo.number_people.get_two()
            case.result = current_result and current_result1 and check_result_1 and check_result_2 and check_result_3
            gettyimage_page.filter.photo.number_people.set_one(0)
            gettyimage_page.filter.photo.number_people.set_two(0)

        with uuid('ea76948b-d351-4c6f-be91-c5712d7a1dc9') as case:
            # Number of People > Group of people
            current_result = gettyimage_page.filter.photo.number_people.set_group(1)
            check_result_1 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            check_result_2 = gettyimage_page.filter.photo.number_people.get_group()
            case.result = current_result and current_result1 and check_result_1 and check_result_2

        with uuid('654ffa1a-23aa-4ad3-8c6b-11a3638d2b7a') as case:
            # Clear all selected filter
            gettyimage_page.click_clear_all_button()
            case.result = not gettyimage_page.filter.photo.number_people.get_group()

        with uuid('1e0adb6f-8f71-47ac-8e5f-eabfe0765317') as case:
            # Search Background
            download_from_shutterstock_page.search.click_clear()
            download_from_shutterstock_page.search.search_text('Background')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'Background' else True
            check_result_2 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            case.result = check_result_1 and check_result_2


        with uuid('c09bcc00-b3a8-4d6c-b220-59f639ca5274') as case:
            # Search Local landmark
            download_from_shutterstock_page.search.click_clear()
            download_from_shutterstock_page.search.search_text('Local landmark')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'Local landmark' else True
            check_result_2 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            case.result = check_result_1 and check_result_2


        with uuid('c10ec9d7-1c62-42db-b148-935a1ac9a440') as case:
            #  Search Sports
            download_from_shutterstock_page.search.click_clear()
            download_from_shutterstock_page.search.search_text('Sports')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'Sports' else True


            check_result_2 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            case.result = check_result_1 and check_result_2


        with uuid('979aa1b3-9f9d-43c5-bfd4-7029c3d5f0f5') as case:
            # Search People
            download_from_shutterstock_page.search.click_clear()
            download_from_shutterstock_page.search.search_text('People')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'People' else True


            check_result_2 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            case.result = check_result_1 and check_result_2

        with uuid('e92e829c-cb98-4736-83e3-8b696012da11') as case:
            # Search Food
            download_from_shutterstock_page.search.click_clear()
            download_from_shutterstock_page.search.search_text('Food')
            download_from_shutterstock_page.find(L.download_from_shutterstock.frame_clips, timeout=30)

            search_keyword = download_from_shutterstock_page.search.get_text()
            check_result_1 = False if not search_keyword == 'Food' else True


            check_result_2 = main_page.exist({'AXIdentifier': 'ShutterstockCollectionViewItem', 'AXIndex': 0})
            case.result = check_result_1 and check_result_2



    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    280a6210-3e68-4200-860b-ca4af846ad46
                    f1b773c7-d746-45da-80f7-c207c3b72094
                    0beb8edd-a547-48fc-aab6-1ba9fbe28c14
                    01a5e01a-81e2-440c-bef7-605e3cb877d1
                    22ea3bce-189a-466b-945f-e22418fd05cb
                    fee11fc9-bc09-41f7-96e3-eb94879a8bb3
                    e7a97c33-aaae-4ad9-91ba-7f3ff87ac024
                    f5c3c3a4-7437-4934-b7ad-fcc170b34406
                    aff169f4-e1f3-4842-b662-758ef9b03f29
                    e6026271-6950-4080-a276-94ceaad25a8b
                    578f32b5-9b2a-4785-b4a5-c539e98b9f15
                    40c942d1-6221-4026-bdaa-bfbeeced66f7
                    82fad090-fda5-46bf-8b00-372357cde8ab
                    2dff1dec-f88a-4404-91d5-0050ba3da735
                    abdeaf10-5d0b-4803-aebe-f1606523048a
                    faf3254f-0e30-4241-879f-efd0dace231b
                    c9e493ef-6ce9-4391-b441-691bc42a8b89
                    f96ff82f-1854-48e6-af2f-3bf34e690105
                    16c2bff9-567c-41b6-b3f5-28c2baa9bb26
                    152041b5-0b4a-4d26-b209-f652d4993cfa
                    8435f5df-69db-4d7e-aa27-96c42defb2d6
                    8f55009a-895e-4da0-87cd-02181d8a338d
                    4273d60e-0453-42e2-8e91-4d17fa2f607c
                    1caae658-9d41-419e-9b00-a97ac371abf6
                    e54e163f-45a4-4061-9a73-92b995d48a0c
                    a8aa0894-b5d5-4d70-9b3b-11acedcb1471
                    50144edc-9b1f-4d4b-8f1e-c7c97d3b8b0f
                    95368c2f-66ee-45c2-8328-2b4c5a7ba5ee
                    ed91d03f-acc2-4d1c-83d3-8b45c6a6d1db
                    90afdab9-b1b7-4abf-9ad7-57f270dbb037
                    97257425-368e-4f12-b178-efaf97e019b2
                    80726031-ca47-4410-b561-d7fc71481416
                    1f11f0f1-a28e-4218-802e-4b85341bb21b
                    dcf789be-8b31-4ddf-91a3-ec9107fde5aa
                    b3a3d985-ef53-4a69-816e-b0c495fc3abb
                    00b64969-c6ed-4f1a-8256-0403299495e4
                    4e7ebbd7-5365-4deb-8f23-02814e3344d4
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'
            media_room_page.enter_downloaded()
            time.sleep(10)
            media_room_page.collection_view_right_click_select_all()
            main_page.press_del_key()
            main_page.press_enter_key()













