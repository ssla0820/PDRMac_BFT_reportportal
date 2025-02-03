import sys, os
from typing import Optional

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
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
effect_room_page = PageFactory().get_page_object('effect_room_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)


# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Effect Room.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder - Setup for Overall Project
Ground_Truth_Folder = app.ground_truth_root + '/Effect_Room/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Effect_Room/'
Test_Material_Folder = app.testing_material

# For Ground Truth / Test Material folder - Setup for Duncan personal testing
#Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/GroundTruth/Effect_Room/'
#Auto_Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/ATGroundTruth/Effect_Room/'
#Test_Material_Folder = '/Users/cl/Desktop/Duncan/Material/Color_LUT/'

DELAY_TIME = 1

class Test_Effect_Room():
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
        main_page.clear_cache()
        # for update the correct module start time of report (2021/04/20)
        now = datetime.datetime.now()
        report.add_ovinfo('time', now.time().strftime("%H:%M:%S"))
        report.start_time = time.time()
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_init('Effect_room')

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
    def test_2_2_4_a(self):
        with uuid("83f9ef2a-28e3-4756-bd07-9b60c86edbc1") as case:
            # 2.2.4 Delete the selected tag - Default tag - The button grays out
            time.sleep(5)
            main_page.enter_room(3)
            effect_room_page.select_specific_tag('Style Effect')
            effect_room_page.right_click()
            time.sleep(1)
            current_image = effect_room_page.snapshot(locator=L.effect_room.library, file_name=Auto_Ground_Truth_Folder + '2-2-4_RightClick_Default.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-2-4_RightClick_Default.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_5_a(self):
        with uuid("669fd01b-fa74-4030-a488-bef50c794486") as case:
            # 2.2.5 Right click on - Default tag - The button grays out
            time.sleep(5)
            main_page.enter_room(3)
            effect_room_page.select_specific_tag('Style Effect')
            effect_room_page.right_click()
            time.sleep(1)
            current_image = effect_room_page.snapshot(locator=L.effect_room.library, file_name=Auto_Ground_Truth_Folder + '2-2-5_RightClick_Default.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-2-5_RightClick_Default.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        with uuid("52819136-5f7d-424e-86d5-ce67290062dc") as case:
            # 1.1.1 Enter Effect Room - Mouse click enter
            time.sleep(5)
            main_page.enter_room(3)
            result_status = effect_room_page.check_effect_room()
            logger(result_status)
            case.result = result_status

        with uuid("ffbb26e1-f169-4890-a5b3-e3b3ce186a0d") as case:
            # 1.1.2 Enter Effect Room - Hotkey enter (F4)
            effect_room_page.tap_ParticleRoom_hotkey()
            effect_room_page.tap_EffectRoom_hotkey()
            result_status = effect_room_page.check_effect_room()
            logger(result_status)
            case.result = result_status

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_1_1(self):
        with uuid("c47fc7f8-0936-41e1-a1db-5fe5f13823d1") as case:
            # 2.1 Select Category - Contents match the selected category
            time.sleep(5)
            effect_room_page.tap_EffectRoom_hotkey()
            effect_room_page.select_LibraryRoom_category('Color LUT')
            time.sleep(1)
            current_image = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1_ContentsmatchCategory.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-1_ContentsmatchCategory.png', current_image)
            case.result = compare_result

        with uuid("e03796a4-eaa2-4aa9-8684-87015ab078db") as case:
            # 2.1 Select Category - Thumbnails show as Details
            effect_room_page.select_LibraryRoom_category('Style Effect')
            result_status = main_page.click_library_details_view()
            logger(result_status)
            case.result = result_status

        with uuid("e4c7880c-8249-40e3-b8b3-2113de2af294") as case:
            # 2.1 Select Category - Thumbnails show as Icon
            result_status = main_page.click_library_icon_view()
            logger(result_status)
            case.result = result_status

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_1_2(self):
        with uuid("6650d98a-34a2-4f5f-b20a-935a5751b109") as case:
            # 2.1 Library menu - Sort by name
            time.sleep(5)
            effect_room_page.tap_EffectRoom_hotkey()
            effect_room_page.select_LibraryRoom_category('Style Effect')
            effect_room_page.select_LibraryMenu_LargeIcons()
            effect_room_page.sort_by_name()
            current_image = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1_SortByName.png')
            #logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-1_SortByName.png', current_image)
            case.result = compare_result

        with uuid("e8b97c1f-8a56-4c2c-8ca6-fed57b40868e") as case:
            # 2.1 Library menu - Sort by type
            effect_room_page.select_LibraryMenu_LargeIcons()
            effect_room_page.sort_by_type()
            current_image = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1_SortByType.png')
            #logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-1_SortByType.png', current_image)
            case.result = compare_result

        with uuid("61fcf0e0-803e-4284-b424-f451b8bbd34a") as case:
            # 2.1 Library menu - Extra Large Icons - Thumbnails show as extra large icons
            effect_room_page.select_LibraryMenu_ExtraLargeIcons()
            current_image = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1_ThumbnailExtraLarge.png')
            #logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-1_ThumbnailExtraLarge.png', current_image)
            case.result = compare_result

        with uuid("bd77b756-198b-4438-b1db-e3453a95c624") as case:
            # 2.1 Library menu - Large Icons - Thumbnails show as large icons
            effect_room_page.select_LibraryMenu_LargeIcons()
            current_image = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1_ThumbnailLarge.png')
            #logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-1_ThumbnailLarge.png', current_image)
            case.result = compare_result

        with uuid("4f1bd5e3-dc4e-4096-aa57-536bcfdf5d0e") as case:
            # 2.1 Library menu - Medium Icons - Thumbnails show as medium icons
            effect_room_page.select_LibraryMenu_MediumIcons()
            current_image = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1_ThumbnailMedium.png')
            #logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-1_ThumbnailMedium.png', current_image)
            case.result = compare_result

        with uuid("5e5f0bfc-767f-4dc3-97f0-6efae3d6d2cb") as case:
            # 2.1 Library menu - Small Icons - Thumbnails show as small icons
            effect_room_page.select_LibraryMenu_SmallIcons()
            current_image = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-1_ThumbnailSmall.png')
            #logger(f"{current_image=}")
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-1_ThumbnailSmall.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_1_3(self):
        with uuid("7018cc98-4c10-4de5-8bd9-b84e43dab384") as case:
            # 2.1 Search the library - Show the contents fit the name input in search bar
            time.sleep(5)
            effect_room_page.tap_EffectRoom_hotkey()
            result_status = effect_room_page.search_and_input_text('pop')
            logger(result_status)
            case.result = result_status

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_1_6(self):
        with uuid("8aeaea79-b980-47f9-864a-8375b7448dbe") as case:
            # 2.1.6 Import Color Presets CLUTs - Successfully import the CLUTs to the Color LUT tag
            time.sleep(5)
            main_page.enter_room(3)
            result_status = effect_room_page.import_CLUTs(app.testing_material + '/Color_LUT/3dl_1.3dl/')
            logger(result_status)
            case.result = result_status

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_1(self):
        with uuid("2fc3bfda-66a1-455b-bd06-d4e8609692f4") as case:
            # 2.2.1 Display/Hide explorer view
            time.sleep(5)
            effect_room_page.tap_EffectRoom_hotkey()
            result_status = effect_room_page.displayhideexplorerview()
            logger(result_status)
            case.result = result_status

        with uuid("435c884c-d5c8-41d3-9623-1b14f8c8c0cb") as case:
            # 2.2.1 Display/Hide explorer view
            result_status = effect_room_page.displayhideexplorerview()
            logger(result_status)
            case.result = result_status

        with uuid("7d337aa7-d9f1-440d-bbb8-902c2f5acebd") as case:
            # 2.2.2 Select tag - Contents match the selected category
            result_status = effect_room_page.select_LibraryRoom_category('Color LUT')
            logger(result_status)
            case.result = result_status

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_3_1(self):
        with uuid("8ce6af83-29e2-4f55-a172-2bb15c1f0177") as case:
            # 2.3.1.a Select template_4by3 - The thumbnail in library is correct (4:3)
            time.sleep(5)
            effect_room_page.tap_EffectRoom_hotkey()
            effect_room_page.drag_EffectRoom_Scroll_Bar(1)
            effect_room_page.hover_library_media('Tiles')
            time.sleep(1)
            effect_room_page.right_click_addto_timeline('Tiles')
            main_page.set_project_aspect_ratio_4_3()
            current_image = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-3-1_4by3_Library.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-1_4by3_Library.png', current_image)
            case.result = compare_result

        with uuid("bd4d22e4-6b81-4d29-aa40-65c6f0e30bf1") as case:
            # 2.3.1.a Select template_4by3 - Preview normal in preview window (4:3)
            main_page.set_project_aspect_ratio_4_3()
            current_image = effect_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '2-3-1_4by3_Preview.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-1_4by3_Preview.png', current_image)
            case.result = compare_result

        with uuid("3dedace2-f2ed-4997-b59a-0751304ae005") as case:
            # 2.3.1.a Select template_4by3 - The thumbnail in library is correct (16:9)
            main_page.set_project_aspect_ratio_16_9()
            current_image = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-3-1_16by9_Library.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-1_16by9_Library.png', current_image)
            case.result = compare_result

        with uuid("5e7c4b99-e860-496d-97b7-c0fd65fea6e5") as case:
            # 2.3.1.a Select template_4by3 - Preview normal in preview window (16:9)
            current_image = effect_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '2-3-1_16by9_Preview.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-1_16by9_Preview.png', current_image)
            case.result = compare_result

        with uuid("8b6e9af3-473c-483a-8f8f-de1539c47be5") as case:
            # 2.3.1.a Select template_4by3 - The thumbnail in library is correct (9:16)
            main_page.set_project_aspect_ratio_9_16()
            current_image = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-3-1_9by16_Library.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-1_9by16_Library.png', current_image)
            case.result = compare_result

        with uuid("bd875ac9-9ca2-4227-9d71-1ba2b595aa6b") as case:
            # 2.3.1.a Select template_4by3 - Preview normal in preview window (9:16)
            current_image = effect_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '2-3-1_9by16_Preview.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-1_9by16_Preview.png', current_image)
            case.result = compare_result

        with uuid("a4960b7c-88de-4eea-9dc0-fb0508562290") as case:
            # 2.3.1.a Select template_4by3 - The thumbnail in library is correct (1:1)
            main_page.set_project_aspect_ratio_1_1()
            current_image = effect_room_page.snapshot(locator=L.media_room.library_listview.main_frame, file_name=Auto_Ground_Truth_Folder + '2-3-1_1by1_Library.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-1_1by1_Library.png', current_image)
            case.result = compare_result

        with uuid("97af485d-f3af-4e6f-bb8a-464e94258a9a") as case:
            # 2.3.1.a Select template_4by3 - Preview normal in preview window (1:1)
            current_image = effect_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '2-3-1_1by1_Preview.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-1_1by1_Preview.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_10(self):
        with uuid("b8922f5b-2543-4ddc-ad34-949a81d02178") as case:
            # 2.2.10 Style Effect - Expend the tag - The style and number are correct
            time.sleep(5)
            main_page.enter_room(3)
            effect_room_page.select_LibraryMenu_LargeIcons()
            effect_room_page.select_specific_tag('Style Effect')
            effect_room_page.unfold({'AXIdentifier': 'RoomTagOutlineViewTextField', 'AXValue': 'Style Effect (85)'})
            time.sleep(1)
            current_image = effect_room_page.snapshot(locator=L.effect_room.library, file_name=Auto_Ground_Truth_Folder + '2-2-10_Number.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-2-10_Number.png', current_image)
            case.result = compare_result

        with uuid("fa95e803-ffa4-4b82-826e-6cd545baac0e") as case:
            # 2.2.10 Style Effect - Mouse over the tag - Show the correct Name, Number, and Preset
            effect_room_page.select_specific_tag('Special')
            time.sleep(2)
            current_image = effect_room_page.snapshot(locator=L.effect_room.library, file_name=Auto_Ground_Truth_Folder + '2-2-10_MouseHover.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-2-10_MouseHover.png', current_image)
            case.result = compare_result

        with uuid("2bed203d-d670-4b90-acbd-b5d622c94ea7") as case:
            # 2.3.2 Mouse over template - Show Effect name, type, HW effect info, and 3D info
            effect_room_page.hover_library_media('Beating')
            time.sleep(2)
            current_image = effect_room_page.snapshot(locator=L.effect_room.library, file_name=Auto_Ground_Truth_Folder + '2-3-2_MouseHover.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-2_MouseHover.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_3_3_1b(self):
        with uuid("a622a7ac-f44a-45a6-b2b6-0fb50c8e6eb5") as case:
            # 2.3.3 Apply to - Add w/ Empty Track - Effect Track
            time.sleep(5)
            main_page.enter_room(3)
            effect_room_page.search_and_input_text('pop')
            effect_room_page.right_click_addto_timeline('Pop Art Wall')
            main_page.set_project_aspect_ratio_16_9()
            current_image = effect_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '2-3-3_Preview.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-3_Preview.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_3_3_1a(self):
        with uuid("0fa97b86-5e74-48f6-95bd-e961283bab42") as case:
            # 2.3.3 Apply to - Add w/ Empty Track - Timeline Clip
            time.sleep(5)
            main_page.insert_media('Skateboard 01.mp4')
            main_page.enter_room(3)
            effect_room_page.search_and_input_text('pop')
            effect_room_page.right_click_addto_timeline('Pop Art Wall')
            current_image = effect_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '2-3-3_Preview-2.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-3_Preview-2.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_3_3_2a(self):
        with uuid("fe71ec81-cf76-475b-936f-6ac02caababa") as case:
            # 2.3.3 Apply to - Add w/ Existed Effect - Timeline clip - Replace effect directly
            time.sleep(5)
            main_page.insert_media('Skateboard 01.mp4')
            main_page.enter_room(3)
            effect_room_page.search_and_input_text('pop')
            main_page.drag_media_to_timeline_playhead_position('Pop Art Wall')
            effect_room_page.cancel_input_text()
            effect_room_page.search_and_input_text('black')
            main_page.drag_media_to_timeline_playhead_position('Black and White')
            current_image = effect_room_page.snapshot(locator=L.library_preview.display_panel, file_name=Auto_Ground_Truth_Folder + '2-3-3_ReplaceEffectDirectly.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-3_ReplaceEffectDirectly.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_3_3_2b(self):
        with uuid("fc7dc73c-81d5-4295-bc91-1647f665e6fb") as case:
            # 2.3.3b Apply to - Add w/ Existed Effect - Effect Track - Display Context menu correctly
            time.sleep(5)
            main_page.insert_media('Skateboard 01.mp4')
            main_page.enter_room(3)
            effect_room_page.search_and_input_text('pop')
            effect_room_page.right_click_addto_timeline('Pop Art Wall')
            effect_room_page.cancel_input_text()
            effect_room_page.search_and_input_text('black')
            effect_room_page.hover_library_media('Black and White')
            result_status = main_page.drag_media_to_timeline_clip('Pop Art Wall', 0, 0, 0)
            logger(result_status)
            case.result = result_status

        with uuid("ee515210-f37a-4ef2-ae7b-38004efcf502") as case:
            # 2.3.3c Apply to - Add w/ Existed Effect - Overwrite - Work correctly
            effect_room_page.tap_Undo_hotkey()
            effect_room_page.hover_library_media('Black and White')
            main_page.drag_media_to_timeline_clip('Pop Art Wall', 0, 0, 0)
            current_image = effect_room_page.snapshot(locator=L.main.timeline.table_view, file_name=Auto_Ground_Truth_Folder + '2-3-3c_Overwrite.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-3c_Overwrite.png', current_image)
            case.result = compare_result

        with uuid("2743df34-a582-4892-95a4-667def8ecbcb") as case:
            # 2.3.3e Apply to - Add w/ Existed Effect - Insert - Work correctly
            effect_room_page.tap_Undo_hotkey()
            effect_room_page.hover_library_media('Black and White')
            main_page.drag_media_to_timeline_clip('Pop Art Wall', 0, 0, 1)
            current_image = effect_room_page.snapshot(locator=L.main.timeline.table_view, file_name=Auto_Ground_Truth_Folder + '2-3-3e.Insert.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-3e.Insert.png', current_image)
            case.result = compare_result

        with uuid("26be7aca-0f24-4eb6-8299-8f2895259b9d") as case:
            # 2.3.3f Apply to - Add w/ Existed Effect - Insert and Move All Clips - Work correctly
            effect_room_page.tap_Undo_hotkey()
            effect_room_page.hover_library_media('Black and White')
            main_page.drag_media_to_timeline_clip('Pop Art Wall', 0, 0, 2)
            current_image = effect_room_page.snapshot(locator=L.main.timeline.table_view, file_name=Auto_Ground_Truth_Folder + '2-3-3f.InsertandMove.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-3f.InsertandMove.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_3_3_3(self):
        with uuid("6998dd9d-50c8-477f-a5dd-161fa56f5b4b") as case:
            # 2.3.3.3 Apply to - Remove - Effect track
            time.sleep(5)
            main_page.insert_media('Skateboard 01.mp4')
            main_page.enter_room(3)
            effect_room_page.search_and_input_text('pop')
            effect_room_page.right_click_addto_timeline('Pop Art Wall')
            main_page.select_timeline_media('Pop Art Wall')
            effect_room_page.tap_Remove_hotkey()
            current_image = effect_room_page.snapshot(locator=L.main.timeline.table_view, file_name=Auto_Ground_Truth_Folder + '2-3-3-3.RemoveEffectTrack.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-3-3-3.RemoveEffectTrack.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_3_4(self):
        with uuid("cff4516a-3450-4742-b584-b28f15e4caad") as case:
            # 2.3.4 Right click menu on template - Add to Timeline - Add selected effect to effect track
            time.sleep(5)
            main_page.insert_media('Skateboard 01.mp4')
            main_page.enter_room(3)
            effect_room_page.search_and_input_text('pop')
            result_status = effect_room_page.right_click_addto_timeline('Pop Art Wall')
            logger(result_status)
            case.result = result_status

        with uuid("524ced19-1b45-41cd-b2ca-b870c7b8ab4c") as case:
            # 2.3.4 Right click menu on template - Add to - My Favorites
            effect_room_page.import_CLUTs(app.testing_material + '/Color_LUT/3dl_1.3dl/')
            effect_room_page.hover_library_media('3dl_1')
            result_status = effect_room_page.right_click_add_to_my_favorites()
            logger(result_status)
            case.result = result_status

        with uuid("b74dad53-1841-4f98-842a-01e443092919") as case:
            # 2.3.4 Right click menu on template - Add to - My Favorites
            time.sleep(1)
            effect_room_page.add_effectroom_new_tag('PDR_Mac_AT_5')
            effect_room_page.hover_library_media('3dl_1')
            result_status = effect_room_page.right_click_addto('PDR_Mac_AT_5')
            logger(result_status)
            case.result = result_status

        with uuid("3f497e9c-5765-46f2-b429-e9879da2f037") as case:
            # 2.3.4 Right click menu on template - Remove from My Favorites
            effect_room_page.hover_library_media('3dl_1')
            result_status = effect_room_page.remove_from_favorites()
            logger(result_status)
            case.result = result_status

        with uuid("769c0f1f-8648-45cf-ac8f-92135378c377") as case:
            # 2.3.4 Right click menu on template - Delete (only for Custom/Downloaded)
            effect_room_page.hover_library_media('3dl_1')
            result_status = effect_room_page.right_click_remove_clut()
            logger(result_status)
            case.result = result_status

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_3(self):
        with uuid("e2aa34c2-39e1-4f59-b0e2-048b3d78c8be") as case:
            # 2.2.3 Add a new tag - Set a new name - Add a new tag
            time.sleep(5)
            effect_room_page.tap_EffectRoom_hotkey()
            time.sleep(1)
            result_status = effect_room_page.add_effectroom_new_tag('PDR_Mac_AT')
            logger(result_status)
            case.result = result_status

        with uuid("344dd09e-f76e-4969-87e2-8ea1a34ebe8f") as case:
            # 2.2.3 Add a new tag - Set a existed name - Pops out warning msg
            time.sleep(1)
            result_status = effect_room_page.add_effectroom_new_tag('PDR_Mac_AT')
            logger(result_status)
            case.result = not result_status

        with uuid("0770155e-2a4b-4888-ad52-1a98cf6aced3") as case:
            # 2.2.3 Add a new tag - Display the unicode tag name normally
            time.sleep(1)
            result_status = effect_room_page.add_effectroom_new_tag('許功蓋')
            logger(result_status)
            case.result = result_status


    # @pytest.mark.skip
    @exception_screenshot
    def test_2_2_4_b(self):
        with uuid("f1e7bed7-3811-455d-a306-3905157acecb") as case:
            # 2.2.4 Right click on selected tag - Custom tag - Delete the selected tag
            time.sleep(5)
            main_page.enter_room(3)
            time.sleep(1)
            effect_room_page.add_effectroom_new_tag('PDR_Mac_AT')
            time.sleep(1)
            result_status = effect_room_page.delete_tag('PDR_Mac_AT')
            logger(result_status)
            case.result = result_status

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_5_b(self):
        with uuid("953c4ed0-841b-44e2-b999-c6d81bc916bc") as case:
            # 2.2.5 Right click on - Custom tag - Rename the tag
            time.sleep(5)
            main_page.enter_room(3)
            time.sleep(1)
            effect_room_page.add_effectroom_new_tag('PDR_Mac_AT')
            time.sleep(1)
            result_status = effect_room_page.right_click_rename_tag(3, 'Renamed')
            logger(result_status)
            case.result = result_status

        with uuid("02f04e26-cf35-4153-a58d-a7c1492ef6ff") as case:
            # 2.2.5 Right click on - Custom tag - Delete the tag
            time.sleep(1)
            result_status = effect_room_page.right_click_delete_tag(3)
            logger(result_status)
            case.result = result_status

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_6_a(self):
        with uuid("71513b05-6dc5-42eb-be92-58b341464700") as case:
            # 2.2.6 save/pack project then reload to check custom tag - Save/Open
            time.sleep(5)
            main_page.enter_room(3)
            time.sleep(2)
            effect_room_page.add_effectroom_new_tag('PDR_Mac_AT_3')
            main_page.save_project("Effect_Room_01", app.testing_material + '/Effect_Room/')
            effect_room_page.import_CLUTs(app.testing_material + '/Color_LUT/3dl_1.3dl/')
            main_page.tap_OpenProject_hotkey()
            main_page.handle_open_project_dialog(app.testing_material + '/Effect_Room/Effect_Room_01.pds/')
            main_page.handle_merge_media_to_current_library_dialog()
            main_page.enter_room(3)
            time.sleep(1)
            current_image = effect_room_page.snapshot(locator=L.effect_room.library, file_name=Auto_Ground_Truth_Folder + '2-2-6_Save_OpenProject.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-2-6_Save_OpenProject.png', current_image)
            case.result = compare_result

    #@pytest.mark.skip
    @exception_screenshot
    def test_2_2_6_b(self):
        with uuid("a07bd5fb-a4dc-4689-9b5b-cf94548029a3") as case:
            # 2.2.6 save/pack project then reload to check custom tag - Pack/Open
            time.sleep(5)
            main_page.enter_room(3)
            time.sleep(2)
            effect_room_page.add_effectroom_new_tag('PDR_Mac_AT_4')
            main_page.top_menu_bar_file_pack_project_materials(app.testing_material + '/Effect_Room/')
            time.sleep(2)
            main_page.tap_OpenProject_hotkey()
            main_page.handle_open_project_dialog(app.testing_material + '/Effect_Room/PackedProject.pds/')
            main_page.handle_merge_media_to_current_library_dialog()
            main_page.enter_room(3)
            time.sleep(1)
            current_image = effect_room_page.snapshot(locator=L.effect_room.library, file_name=Auto_Ground_Truth_Folder + '2-2-6_Pack_OpenProject.png')
            compare_result = effect_room_page.compare(Ground_Truth_Folder + '2-2-6_Pack_OpenProject.png', current_image)
            case.result = compare_result