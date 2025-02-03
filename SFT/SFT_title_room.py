import sys, os

from SFT.globals import update_report_info, get_enable_case_execution_log, google_sheet_execution_log_init, \
    google_sheet_execution_log_update_result

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
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)


# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Title Room.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder - Setup for Overall Project
Ground_Truth_Folder = app.ground_truth_root + '/Title_Room/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Title_Room/'
Test_Material_Folder = app.testing_material

# For Ground Truth / Test Material folder - Setup for Duncan personal testing
# Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/GroundTruth/Title_Room/'
# Auto_Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/ATGroundTruth/Title_Room/'
# Test_Material_Folder = '/Users/cl/Desktop/Duncan/Material/'

DELAY_TIME = 1

class Test_Title_Room():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        yield mwc
        main_page.close_app()

    @classmethod
    def setup_class(cls):
        # for update the correct module start time of report (2021/04/20)
        main_page.clear_cache()
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('Title_Room')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"test case template result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                               report.get_ovinfo('skip'),
                               report.get_ovinfo('duration'))
        report.show()

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        with uuid("e65f3e12-1dfc-40f6-b80f-1c23f3b8723a") as case:
            # 1.1.1 Mouse click enter - enter title room
            time.sleep(5)
            title_room_page.enter_room(1)
            result_status = title_room_page.check_in_title_room()
            logger(result_status)
            case.result = result_status

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_1_1(self):
        with uuid("be295edc-bfd2-41e3-bf08-77eef2cdc975") as case:
            # 2.1.1 Import media - Import Title Templates
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            result_status = title_room_page.click_ImportTitleTemplates(app.testing_material + '/TitleTemplate_1.dzt')
            time.sleep(1)
            title_room_page.click_OK_onEffectExtractor()
            logger(result_status)
            case.result = result_status

        with uuid("fea90ac9-dec7-4393-8024-8684485e0e1e") as case:
            # 2.3.5 Right click menu on template - Remove selected template
            time.sleep(2)
            media_room_page.select_media_content('G3160...')
            time.sleep(2)
            result_status = title_room_page.select_RightClickMenu_Delete()
            logger(result_status)
            case.result = result_status

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_3_3(self):
        with uuid("55a1ec58-1028-4ced-bf15-76de4b0dd003") as case:
            # 2.3.3 Select template - 4by3 - The thumbnail in library is correct
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.select_LibraryRoom_category('Text Only')
            title_room_page.select_LibraryMenu_ExtraLargeIcons()
            title_room_page.set_project_aspect_ratio_4_3()
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-3-3_4by3_Library.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-3-3_4by3_Library.png', current_image)
            case.result = compare_result

        with uuid("c1d3cad3-d1c5-42ac-ab4f-8bccf9751cff") as case:
            # 2.3.3 Select template - 4by3 - Preview normal in preview window
            current_image = title_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '2-3-3_4by3_Preview.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-3-3_4by3_Preview.png', current_image)
            case.result = compare_result

        with uuid("9d1181b7-b28f-4627-ba23-69c37aa11257") as case:
            # 2.3.3 Select template - 16by9 - The thumbnail in library is correct
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.select_LibraryRoom_category('Text Only')
            title_room_page.select_LibraryMenu_ExtraLargeIcons()
            title_room_page.set_project_aspect_ratio_16_9()
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-3-3_16by9_Library.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-3-3_16by9_Library.png', current_image)
            case.result = compare_result

        with uuid("bbe79684-5b1b-471c-9576-ad739157bd93") as case:
            # 2.3.3 Select template - 16by9 - Preview normal in preview window
            current_image = title_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '2-3-3_16by9_Preview.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-3-3_16by9_Preview.png', current_image)
            case.result = compare_result

        with uuid("8416127c-5350-4c28-be2e-767124f5a8b8") as case:
            # 2.3.3 Select template - 9by16 - The thumbnail in library is correct
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.select_LibraryRoom_category('Text Only')
            title_room_page.select_LibraryMenu_ExtraLargeIcons()
            title_room_page.set_project_aspect_ratio_9_16()
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-3-3_9by16_Library.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-3-3_9by16_Library.png', current_image)
            case.result = compare_result

        with uuid("d3e52cce-ce03-493b-a2f3-45f895dc5236") as case:
            # 2.3.3 Select template - 9by16 - Preview normal in preview window
            current_image = title_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '2-3-3_9by16_Preview.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-3-3_9by16_Preview.png', current_image)
            case.result = compare_result

        with uuid("1fffc801-d5e5-47fc-95ec-1025d141e326") as case:
            # 2.3.3 Select template - 1by1 - The thumbnail in library is correct
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.select_LibraryRoom_category('Text Only')
            title_room_page.select_LibraryMenu_ExtraLargeIcons()
            title_room_page.set_project_aspect_ratio_1_1()
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-3-3_1by1_Library.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-3-3_1by1_Library.png', current_image)
            case.result = compare_result

        with uuid("cee36dbd-a556-4188-ae34-7492f6e0a8f7") as case:
            # 2.3.3 Select template - 1by1 - Preview normal in preview window
            current_image = title_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '2-3-3_1by1_Preview.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-3-3_1by1_Preview.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_5_a(self):
        with uuid("08bd0d42-99b2-4128-8793-628ecd84ae36") as case:
            #  2.2.5 Right click on Default tag - All selections gray out
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.select_specific_tag('Text Only')
            title_room_page.right_click()
            current_image = title_room_page.snapshot(locator=L.title_room.explore_view_region.table_all_content_tags, file_name=Auto_Ground_Truth_Folder + '2-2-5-a_RightClick.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-2-5-a_RightClick.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_4_a(self):
        with uuid("70f5eff2-ae1d-41b4-b948-c8560c7dada7") as case:
            # 2.2.4 Delete the selected tag - Default tag - The button grays out
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.select_specific_tag('Text Only')
            title_room_page.right_click()
            current_image = title_room_page.snapshot(locator=L.title_room.explore_view_region.table_all_content_tags, file_name=Auto_Ground_Truth_Folder + '2-2-4_ButtonGrayOut.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-2-4_ButtonGrayOut.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid("f64ce709-e788-4e84-bac2-1f9fca810e3f") as case:
            # 1.1.2 Hotkey enter (F7)
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            result_status = title_room_page.check_in_title_room()
            logger(result_status)
            case.result = result_status

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_1_1_1(self):
        with uuid("be295edc-bfd2-41e3-bf08-77eef2cdc975") as case:
            # 2.1.1 Import media - Import Title Templates
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            result_status = title_room_page.click_ImportTitleTemplates(app.testing_material + '/TitleTemplate_1.dzt/')
            time.sleep(1)
            title_room_page.click_OK_onEffectExtractor()
            logger(result_status)
            case.result = result_status

        with uuid("fea90ac9-dec7-4393-8024-8684485e0e1e") as case:
            # 2.3.5 Right click menu on template - Remove selected template
            media_room_page.select_media_content('G3160...')
            result_status = title_room_page.select_RightClickMenu_Delete()
            logger(result_status)
            case.result = result_status

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_1_2(self):
        with uuid("91ec2e92-582d-4233-8c0c-072c40b6c6e9") as case:
            # 2.1.1 Import media - Download More Title Effects
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            result_status = title_room_page.click_DownloadContent_from_DZCL()
            logger(result_status)
            case.result = result_status

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_1_3(self):
         with uuid("daaa5708-cd85-45c8-b9fa-6ebdffc2b587") as case:
            # 2.1.3 Select Category - Contents match the selected category
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.select_specific_tag('Sporty')
            title_room_page.select_LibraryMenu_LargeIcons()
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1-3_ContentMatchCategory.png')
            #logger(f"{current_image=}")
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-1-3_ContentMatchCategory.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_1_8(self):
        with uuid("5564a29d-0315-4ed9-8274-4e93139244c9") as case:
            # 2.1.8 Library menu - Sort by name
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.set_project_aspect_ratio_16_9()
            title_room_page.select_specific_tag('Motion Graphics')
            title_room_page.select_LibraryMenu_LargeIcons()
            title_room_page.sort_by_name()
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1-8_SortByName.png')
            #logger(f"{current_image=}")
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-1-8_SortByName.png', current_image)
            case.result = compare_result

        with uuid("31560a3a-295c-4d1e-8c95-521ba8931446") as case:
            # 2.1.8 Library menu - Sort by category
            title_room_page.select_LibraryMenu_LargeIcons()
            title_room_page.sort_by_category()
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1-8_SortByCategory.png')
            #logger(f"{current_image=}")
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-1-8_SortByCategory.png', current_image)
            case.result = compare_result

        with uuid("f7551626-9a78-42f2-a7d1-b713fea3891d") as case:
            # 2.1.8 Library menu - Sort by create date
            title_room_page.select_LibraryMenu_LargeIcons()
            title_room_page.sort_by_createdate()
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1-8_SortByCreateDate.png')
            #logger(f"{current_image=}")
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-1-8_SortByCreateDate.png', current_image)
            case.result = compare_result

        with uuid("b219fa4c-b4ab-4d72-aded-e081d5a17c6c") as case:
            # 2.1.8 Library menu - Extra Large Icons - Thumbnails show as extra large icons
            title_room_page.select_specific_tag('Sporty')
            title_room_page.select_LibraryMenu_ExtraLargeIcons()
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1-8_ThumbnailExtraLarge.png')
            #logger(f"{current_image=}")
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-1-8_ThumbnailExtraLarge.png', current_image)
            case.result = compare_result

        with uuid("28fb1211-876d-4ad8-a469-a85c1032fa47") as case:
            # 2.1.8 Library menu - Large Icons - Thumbnails show as large icons
            title_room_page.select_specific_tag('Sporty')
            title_room_page.select_LibraryMenu_LargeIcons()
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1-8_ThumbnailLarge.png')
            #logger(f"{current_image=}")
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-1-8_ThumbnailLarge.png', current_image)
            case.result = compare_result

        with uuid("135b4209-4378-4de9-b226-72135e919ed2") as case:
            # 2.1.8 Library menu - Medium Icons - Thumbnails show as medium icons
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.select_specific_tag('Sporty')
            title_room_page.select_LibraryMenu_MediumIcons()
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1-8_ThumbnailMedium.png')
            #logger(f"{current_image=}")
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-1-8_ThumbnailMedium.png', current_image)
            case.result = compare_result

        with uuid("c4b71039-7539-4b8a-9b0c-7a3248198aec") as case:
            # 2.1.8 Library menu - Small Icons - Thumbnails show as small icons
            title_room_page.select_LibraryMenu_SmallIcons()
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1-8_ThumbnailSmall.png')
            logger(f"{current_image=}")
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-1-8_ThumbnailSmall.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_1_10(self):
        with uuid("8ab0ab12-18d6-4a70-9bd6-8e907e87166c") as case:
            # 2.1.10 Search the library - Show the contents fit the name input in search bar
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.select_LibraryRoom_category('Motion Graphics')
            title_room_page.select_LibraryMenu_MediumIcons()
            title_room_page.search_Title_room_library('5')
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1-10_Search.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-1-10_Search.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_1(self):
         with uuid("38b8edf2-194e-4389-ae71-2b21c99328fc") as case:
            # 2.2.1 Display/Hide explorer view - Display the explorer view
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            result_status = title_room_page.click_ExplorerView()
            logger(result_status)
            case.result = result_status

         with uuid("140d153e-abad-4dd8-8edd-adefed66845d") as case:
             # 2.2.1 Display/Hide explorer view - Hide the explorer view
             title_room_page.click_ExplorerView()
             result_status = title_room_page.click_ExplorerView()
             logger(result_status)
             case.result = result_status


    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_2(self):
        with uuid("ec1c9eda-4ec2-4781-92dc-5cc88987413d") as case:
            # 2.2.2 Select tag - Contents match the selected category
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.click_ExplorerView()
            title_room_page.select_LibraryRoom_category('Text Only')
            title_room_page.select_LibraryMenu_MediumIcons()
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-2-2_SelectTag.png')
            #logger(f"{current_image=}")
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-2-2_SelectTag.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_3_5_a(self):
        with uuid("353b70d7-622e-43ea-915c-dd094fdfb7f6") as case:
            # 2.2.5 Right click menu on template - Add to Timeline - Add right clicked clip to selected track
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.select_LibraryRoom_category('General')
            media_room_page.select_media_content('Clover_02')
            title_room_page.select_RightClickMenu_AddToTimeline()
            timeline_image = title_room_page.snapshot(locator=title_room_page.area.timeline, file_name=Auto_Ground_Truth_Folder + '2-3-5_AddtoTimeline.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-3-5_AddtoTimeline.png', timeline_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_1_6(self):
        with uuid("dd417c68-13a5-448a-9620-fab0a71e5575") as case:
            # 2.1.6 Details view
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.select_LibraryRoom_category('Motion Graphics')
            result_status = title_room_page.click_library_details_view()
            logger(result_status)
            case.result = result_status

        with uuid("8583ca38-eb38-44ad-a96b-180546264e8e") as case:
            # 2.1.7 Icon view
            time.sleep(1)
            result_status = title_room_page.click_library_icon_view()
            logger(result_status)
            case.result = result_status

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_3_a(self):
        with uuid("ae8c064a-8e25-40cd-a28a-1228ca5c82e8") as case:
            # 2.2.3 Add a new tag - Set a new name
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            time.sleep(1)
            result_status = title_room_page.add_titleroom_new_tag('PDR_Mac_AT')
            logger(result_status)
            case.result = result_status

        with uuid("7d85a3d1-7b76-492c-8682-6e2e872ca8c2") as case:
            # 2.2.3 Add a new tag - Pops out warning msg
            time.sleep(1)
            title_room_page.tap_TitleRoom_hotkey()
            time.sleep(1)
            result_status = title_room_page.add_titleroom_new_tag('PDR_Mac_AT')
            logger(result_status)
            case.result = not result_status

            # if execute completed then revert to initial status:
            #if title_room_page.find_specific_tag('PDR_Mac_AT'):
                #title_room_page.right_click_delete_tag('PDR_Mac_AT')
            #if title_room_page.find_specific_tag('New Tag'):
                #title_room_page.right_click_delete_tag('New Tag')

        with uuid("f4fdf85c-847c-435c-b102-d31ef5fff5ec") as case:
            # 2.2.3 Add a new tag - Display the unicode tag name normally
            time.sleep(1)
            result_status = title_room_page.add_titleroom_new_tag('???')
            logger(result_status)
            case.result = result_status

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_2_6(self):
        with uuid("0b2d756f-47b3-4550-8e6c-f0cf4cb45039") as case:
            #  2.2.6 Keep tag after re-launch PDR
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            current_image = title_room_page.snapshot(locator=L.title_room.explore_view_region.table_all_content_tags, file_name=Auto_Ground_Truth_Folder + '2-2-6_Keeptag.png')
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-2-6_Keeptag.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_1_4(self):
        with uuid("c26bd196-0e0c-4364-adad-0144cd6ebf21") as case:
            #  2.1.4 Create a new title template - Enter Title Designer
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.click_CreateNewTitle_btn()
            result_status = title_room_page.check_enter_title_designer()
            logger(result_status)
            case.result = result_status

    @exception_screenshot
    def test_2_1_5(self):
        with uuid("1dcf2967-53c4-40ea-b75d-fc9757755910") as case:
            #  2.1.5 Modify the selected title template - Enter Title Designer
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.select_LibraryRoom_category('Text Only')
            media_room_page.select_media_content('Default')
            title_room_page.select_RightClickMenu_ModifyTemplate()
            result_status = title_room_page.check_enter_title_designer()
            logger(result_status)
            case.result = result_status

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_3_5_b(self):
        with uuid("7683e1c8-505a-4548-974e-6500128c10d0") as case:
            #  2.3.5 Modify the selected title template - Modify Template?
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.select_LibraryRoom_category('Text Only')
            media_room_page.select_media_content('Default')
            result_status = title_room_page.select_RightClickMenu_ModifyTemplate()
            logger(result_status)
            case.result = result_status

    @exception_screenshot
    def test_2_3_5_c(self):
        with uuid("c5c1dd57-0799-486f-b12d-ccb18416324d") as case:
            #  2.3.5 Modify the selected title template - Add to custom tag
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.select_LibraryRoom_category('Text Only')
            media_room_page.select_media_content('Default')
            time.sleep(1)
            result_status = title_room_page.select_RightClickMenu_Addto('???')
            time.sleep(1)
            logger(result_status)
            case.result = result_status

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_5_b(self):
        with uuid("371a91f6-05a8-4252-89ec-2ea55654afc7") as case:
            #  2.2.5 Right click on Custom tag - Rename the tag
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            result_status = title_room_page.select_tag_RightClickMenu_RenameTag('PDR_Mac_AT', 'Renamed')
            logger(result_status)
            case.result = result_status

        with uuid("85d1f653-bf90-4046-be67-7b34983e39e8") as case:
            #  2.2.5 Right click on Custom tag - Delete the tag
            title_room_page.tap_TitleRoom_hotkey()
            result_status = title_room_page.select_tag_RightClickMenu_DeleteTag('Renamed')
            logger(result_status)
            case.result = result_status

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_3_1(self):
        with uuid("e7cbca2d-9c5a-476f-8ad4-de76902ba7a6") as case:
            #  2.3.1 Free Templates - Link to DZ Title download website
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.click_freeTemplate()
            time.sleep(5)
            result_status = title_room_page.check_chrome_page()
            logger(result_status)
            case.result = result_status

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_3_4_a(self):
        with uuid("484044cd-5d34-494e-af05-ebc189f9fd5f") as case:
            #  2.3.4 Mouse over template - Click DZ icon - Link to the title template in DZ website
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.click_freeTemplate()
            time.sleep(5)
            result_status = title_room_page.check_chrome_page()
            logger(result_status)
            case.result = result_status

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_3_4_b(self):
        with uuid("e796bd3d-d735-4057-a286-e8b86d71b6e3") as case:
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            title_room_page.select_LibraryMenu_LargeIcons()
            title_room_page.select_LibraryRoom_category('Text Only')
            title_room_page.hover_library_media('Wave')
            time.sleep(3)
            current_image = title_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-3-4_Showtitlename.png')
            # logger(f"{current_image=}")
            compare_result = title_room_page.compare(Ground_Truth_Folder + '2-3-4_Showtitlename.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_4_b(self):
        with uuid("5565c3af-c0a8-4447-9481-99e086393500") as case:
            # 2.2.4 Delete the selected tag - Custom tag - Delete the tag
            time.sleep(5)
            title_room_page.tap_TitleRoom_hotkey()
            time.sleep(1)
            title_room_page.add_titleroom_new_tag('PDR_Mac_AT_2')
            result_status = title_room_page.select_tag_RightClickMenu_DeleteTag('New Tag')
            logger(result_status)
            case.result = result_status

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    e81ffdfe-9b46-432c-a71e-67906c96893b
                    0d5f67ea-78f9-49a2-ae34-807008064006
                    8075312f-065d-4e09-8345-8e3aa17ff8d6
                    8583ca38-eb38-44ad-a96b-180546264e8e
                    3bba4eb7-bd0e-40e7-87fa-53deb84734b5
                    927310a5-c719-4de1-a8ec-8498ec242111
                    142f65e5-0ab6-4f4e-9a4c-d0a2a719e841
                    172fe31f-c26f-42b5-bab2-5fa706865ab4
                ''') as case:
            case.result = None
            case.fail_log = "*SKIP by AT*"