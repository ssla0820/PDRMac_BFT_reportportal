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
mwc = DriverFactory().get_mac_driver_object('mac', app.app_name, app.app_bundleID, app.app_path)
main_page = PageFactory().get_page_object('main_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
pip_designer_page = PageFactory().get_page_object('pip_designer_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="PiP Object Room.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/PiP_Room/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/PiP_Room/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

# @pytest.fixture(scope="module", autouse= True)
# def init():
#     yield
#     main_page.close_app()
#     report.export()
#     report.show()


class Test_PiP_Object_Room():
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
            google_sheet_execution_log_init('PiP_Room')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"pip room result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
        update_report_info(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                           report.get_ovinfo('skip'),
                           report.get_ovinfo('duration'))
        # for test case module google sheet execution log (2021/04/12)
        if get_enable_case_execution_log():
            google_sheet_execution_log_update_result(report.get_ovinfo('pass'), report.fail_number, report.get_ovinfo('na'),
                                                     report.get_ovinfo('skip'), report.get_ovinfo('duration'))
        report.show()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_1(self):
        with uuid('4c48025a-fe5d-4d5e-9d39-ee360e041f6e') as case:
            # 1. General
            # 1.1. Enter PiP Room
            # 1.1.1. Mouse click enter > enter PiP Object Room
            main_page.enter_room(4)

            check_result = pip_room_page.check_in_Pip_room()
            case.result = check_result
            main_page.enter_room(0)

        with uuid('36f3aaed-3d2a-4977-b5a6-cfcbb4e89372') as case:
            # 1.1.2. Hotkey enter (F5) > enter pip object room
            pip_room_page.tap_PiPRoom_hotkey()
            # with transition_room_page.keyboard.pressed(main_page.keyboard.key.f5):
            #     pass
            check_result = pip_room_page.check_in_Pip_room()
            case.result = check_result

        with uuid('5f82836f-a5fc-4235-820e-79fc1de27b99') as case:
            # 2. Function
            # 2.1. Function bar
            # 2.1.1 Import media > import PiP Templates > import downloaded pip template files successfully
            pip_room_page.click_ImportPiPObject(Test_Material_Folder + '2144330281-1615752299605.dzp')
            time.sleep(DELAY_TIME*3)
            pip_room_page.click_OK_onEffectExtractor()

            # check import process success
            check_result = pip_room_page.check_is_in_Downloaded_category('Frame5317')
            case.result = check_result

        with uuid('cf00ab57-d3ec-4884-b4f3-e03e69f313c6') as case:
            # 2.1. Function bar
            # 2.1.1 Import media > download more pip effects > log in to CL Cloud to download pip templates
            pip_room_page.download_Content_from_Cloud('00-PiPObject')

            # check import process success
            check_result = pip_room_page.check_is_in_Downloaded_category('00-PiPObject')
            case.result = check_result

        with uuid('38cefb67-c003-4271-9ec7-fb9a016b5790') as case:
            # 2.1. Function bar
            # 2.1.3. select category > contents match the selected category
            pip_room_page.select_LibraryRoom_category('Romance')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_1_3_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_1_3_1.png'
            current_preview = pip_room_page.snapshot(
                locator=L.pip_room.explore_view_region.table_all_content_tags,
                file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('a373b823-6d3a-4c8f-9498-c99f0d7a211a') as case:
            # 2.1. Function bar
            # 2.1.4. create a new pip object from an image > enter folder to select an image and then enter pip designer
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')

            check_result = pip_room_page.check_in_PiP_designer()
            case.result = check_result

            # pip designer page function not ready, cannot create a custom pip object
            pip_room_page.press_esc_key()

        # with uuid('38c5be55-4818-4432-8304-03fa5ae296d3') as case:
        #     # pip designer page function is not ready
        #     # 2.1. Function bar
        #     # 2.1.2. upload to DZ/CL cloud > enter upload page
        #     # check_result = pip_room_page.click_Upload_toDZCL_btn()
        #     case.result = None

        with uuid('35ec6dbb-05ae-4258-8fea-9a556e5ea02b') as case:
            # 2.1.7. Function bar > modify the selected pip template > select pip template
            # pip designer
            pip_room_page.click_ModifyAttribute_btn('PiP')
            check_result = pip_room_page.check_in_PiP_designer()
            case.result = check_result

            # leave pip designer
            pip_room_page.press_esc_key()
            # with pip_room_page.keyboard.pressed(main_page.keyboard.key.esc):
            #     pass

        with uuid('58b07b1e-b951-4ea1-9d6a-4cd3177aa3b3') as case:
            # 2.1.7. Function bar > modify the selected pip template > select pip template
            # mask designer
            check_result = pip_room_page.click_ModifyAttribute_btn('Mask')
            case.result = check_result

            # leave mask designer
            pip_room_page.press_esc_key()
            # with pip_room_page.keyboard.pressed(main_page.keyboard.key.esc):
            #     pass

        with uuid('70abf524-8e80-4954-8f89-00ec3a6c8cd0') as case:
            # 2.1. Function bar
            # 2.1.8. detail view > thumbnails show as details
            pip_room_page.select_LibraryRoom_category('All Content')
            main_page.click_library_details_view()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_1_8_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_1_8_1.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.scroll_area.library_table_view, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('e04cbb7f-a940-4fcf-a962-d6302178062d') as case:
            # 2.1. Function bar
            # 2.1.9. icon view > thumbnails show as icon
            main_page.click_library_icon_view()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_1_9_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_1_9_1.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('d68bf959-0ec7-4051-b805-89c0cefaeb4e') as case:
            # 2.1. Function bar
            # 2.1.10. library menu > sort by > category
            pip_room_page.sort_by_category()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_1_10_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_1_10_1.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('e711c0aa-ef51-4707-a0bc-d8a8c70664b0') as case:
            # 2.1. Function bar
            # 2.1.10. library menu > sort by > created date
            pip_room_page.sort_by_created_date()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_1_10_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_1_10_3.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('91c1d652-118c-43ce-a9c5-a454f1019f09') as case:
            # 2.1. Function bar
            # 2.1.10. library menu > sort by > name
            pip_room_page.sort_by_name()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_1_10_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_1_10_2.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('9ab432f2-e049-42d9-9ee2-fd1333b5c291') as case:
            # 2.1. Function bar
            # 2.1.10. library menu > extra large icons
            pip_room_page.select_LibraryMenu_ExtraLargeIcons()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_1_10_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_1_10_4.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('5a450906-b817-428a-8b0f-0d208fa27ad2') as case:
            # 2.1. Function bar
            # 2.1.10. library menu > large icons
            pip_room_page.select_LibraryMenu_LargeIcons()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_1_10_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_1_10_5.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('0746b2f8-d98c-4c54-81fd-429ca2640f82') as case:
            # 2.1. Function bar
            # 2.1.10. library menu > small icons
            pip_room_page.select_LibraryMenu_SmallIcons()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_1_10_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_1_10_7.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('07b6d155-b8bd-4b99-8a02-56107b1108f9') as case:
            # 2.1. Function bar
            # 2.1.10. library menu > medium icons
            pip_room_page.select_LibraryMenu_MediumIcons()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_1_10_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_1_10_6.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('36127c1f-8213-4dab-945c-a5b1974578d3') as case:
            # 2.1. Function bar
            # 2.1.12. search the library > show the contents fit the name input in search bar
            pip_room_page.search_PiP_room_library('Wedding')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_1_10_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_1_10_8.png'
            current_preview = pip_room_page.snapshot(
                locator=pip_room_page.area.library_icon_view, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

    @exception_screenshot
    def test_1_1_2(self):
        with uuid('7e77930e-85a2-4200-90c7-9b3446dcb56b') as case:
            # 2.2. Explorer view
            # 2.2.1. Display/Hide explorer view > Hide
            # hide the explorer view
            main_page.enter_room(4)

            pip_room_page.click_ExplorerView()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_2_1_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_2_1_2.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('c84ae1c5-553b-4c36-8776-fab87d01b99b') as case:
            # 2.2.1. Display/Hide explorer view > display
            # display the explorer view
            pip_room_page.click_ExplorerView()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_2_1_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_2_1_1.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('ded0d0bd-b877-457b-a3ce-ffc02c924547') as case:
            # 2.2.2. Select tag
            # contents math the selected category
            pip_room_page.select_LibraryRoom_category('Romance')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_2_2_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_2_2_1.png'
            current_preview = pip_room_page.snapshot(
                locator=L.pip_room.explore_view_region.table_all_content_tags,
                file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('e8aff1e3-b033-4db3-8cc7-a2ad345a9426') as case:
            # 2.2.3. Add a new tag > set a new name
            # add a new tag
            pip_room_page.add_new_tag('test_tag')

            check_result = pip_room_page.find_specific_tag('test_tag')
            case.result = check_result

        with uuid('190a10dc-f0ca-4725-a39a-9b098dd3df25') as case:
            # 2.2.3. Add a new tag > set a existed name
            # pops out warning msg
            check_result = pip_room_page.add_new_tag('test_tag')

            if not check_result:
                case.result = True
            else:
                case.result = False

        with uuid('4c2a81f6-6511-48d7-bce9-4162c11eb1f4') as case:
            # 2.2.3. Add a new tag > unicode
            # display the unicode tag name normally
            pip_room_page.add_new_tag('許功蓋')

            check_result = pip_room_page.find_specific_tag('許功蓋')
            case.result = check_result

        with uuid('5e85232f-a17a-4e64-877a-c6099a13213c') as case:
            # 2.2.4. Delete the selected tag > Default tag
            # the button grays out
            pip_room_page.select_specific_tag('Romance')

            check_result = pip_room_page.get_status_DeleteSelectedTag()
            if not check_result:
                case.result = True
            else:
                case.result = False

        with uuid('1dcd8a88-97be-492e-a703-8a20e656afc9') as case:
            # 2.2.4. Delete the selected tag > custom tag
            # delete the selected tag
            pip_room_page.delete_tag('許功蓋')

            check_result = pip_room_page.find_specific_tag('許功蓋')
            if not check_result:
                case.result = True
            else:
                case.result = False

        with uuid('fd1e2f5c-8e0d-46a8-885e-82e54f4e3fe3') as case:
            # 2.2.5. Right click on > default tag
            # all selections gray out
            pip_room_page.select_specific_tag('Romance')
            pip_room_page.right_click()

            check_result_1 = pip_room_page.get_status_rightclickmenu_RenameTag()
            check_result_2 = pip_room_page.get_status_rightclickmenu_DeleteTag()

            check_result = check_result_1 and check_result_2
            if not check_result:
                case.result = True
            else:
                case.result = False

            pip_room_page.select_specific_tag('All Content')

        with uuid('0d01a966-2d17-43bb-893b-b1bfac81a984') as case:
            # 2.2.5. Right click on > custom tag
            # rename tag
            pip_room_page.select_tag_RightClickMenu_RenameTag('New Tag', 'Rename_Tag')
            check_result = pip_room_page.find_specific_tag('Rename_Tag')
            if not check_result:
                case.result = False
            else:
                case.result = True

        with uuid('e362c1a6-ebdc-495d-af3e-0dd63f204317') as case:
            # 2.2.5. Right click on > custom tag
            # delete tag
            pip_room_page.select_tag_RightClickMenu_DeleteTag('Rename_Tag')
            check_result = pip_room_page.find_specific_tag('Rename_Tag')
            if not check_result:
                case.result = True
            else:
                case.result = False

        with uuid('b9a0b83f-ff00-414e-8152-083db0a39ebb') as case:
            # 2.2.6. save/pack project then reload to check custom tag > save and open
            # the custom tags show normally
            main_page.save_project('test_pip_custom_tag_save', Test_Material_Folder)
            time.sleep(DELAY_TIME)
            main_page.close_and_restart_app()
            main_page.top_menu_bar_file_open_project()
            main_page.handle_open_project_dialog(Test_Material_Folder + 'test_pip_custom_tag_save.pds')
            main_page.handle_merge_media_to_current_library_dialog()
            main_page.enter_room(4)

            check_result = pip_room_page.find_specific_tag('test_tag')
            if not check_result:
                case.result = False
            else:
                case.result = True

    @exception_screenshot
    def test_1_1_3(self):
        with uuid('2dbff753-1cae-4a63-9c6e-8ce5d3c1eed6') as case:
            # 2.3. Content area
            # 2.3.2. Select template > 4:3 > thumbnail
            # the thumbnail in library is correct
            main_page.enter_room(4)
            main_page.set_project_aspect_ratio_4_3()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_3_2_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_3_2_1.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('e33ca2f4-c722-4920-b5f1-c13c0e3198f7') as case:
            # 2.3.2. Select template > 4:3 > Preview
            # Preview normal in preview window
            time.sleep(DELAY_TIME)
            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_3_2_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_3_2_2.png'
            current_preview = pip_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('45b7a86e-1aaa-4bdd-acbb-4432b5497a1c') as case:
            # 2.3. Content area
            # 2.3.2. Select template > 9:16 > thumbnail
            # the thumbnail in library is correct
            main_page.set_project_aspect_ratio_9_16()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_3_2_5.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_3_2_5.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('1f83e915-ac5b-4291-a009-b0543db34734') as case:
            # 2.3.2. Select template > 9:16 > Preview
            # Preview normal in preview window
            time.sleep(DELAY_TIME)
            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_3_2_6.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_3_2_6.png'
            current_preview = pip_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('0326dbc8-6740-4c21-bc17-b2a795cc95e7') as case:
            # 2.3. Content area
            # 2.3.2. Select template > 1:1 > thumbnail
            # the thumbnail in library is correct
            main_page.set_project_aspect_ratio_1_1()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_3_2_7.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_3_2_7.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('1cdbdbde-67b5-44a4-ab7c-f2b2f246e2c7') as case:
            # 2.3.2. Select template > 1:1 > Preview
            # Preview normal in preview window
            time.sleep(DELAY_TIME)
            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_3_2_8.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_3_2_8.png'
            current_preview = pip_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('2b24c166-47f3-402a-864a-1e7e61f5c419') as case:
            # 2.3. Content area
            # 2.3.2. Select template > 16:9 > thumbnail
            # the thumbnail in library is correct
            main_page.set_project_aspect_ratio_16_9()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_3_2_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_3_2_3.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('0a0c42cf-e696-4eb9-9e50-1de263833468') as case:
            # 2.3.2. Select template > 16:9 > Preview
            # Preview normal in preview window
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.left_click()
            time.sleep(DELAY_TIME * 4)
            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_3_2_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_3_2_4.png'
            current_preview = pip_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('102aa2fa-c7da-44a4-bb40-8a41d2dee8ac') as case:
            # 2.3.4. Right click menu on template > Add to timeline
            # add right clicked clip to selected track
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_AddToTimeline()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_3_4_1.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_3_4_1.png'
            current_preview = pip_room_page.snapshot(
                locator=pip_room_page.area.timeline, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('189ac53e-e098-4113-a612-831db053d0ef') as case:
            # 2.3.4. Right click menu on template > change alias
            # change clip name in library
            pip_room_page.click_CreateNewPiP_btn(Test_Material_Folder + 'lake_001.jpg')
            pip_designer_page.save_as_name('')
            pip_designer_page.input_template_name_and_click_ok('lake')
            pip_designer_page.click_cancel()
            # pip_room_page.select_specific_tag('Custom')
            pip_room_page.hover_library_media('lake')
            pip_room_page.select_RightClickMenu_ChangeAlias('001_lake')

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_3_4_2.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_3_4_2.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('bd25bd2d-5bd3-4983-a928-fae63eb725c0') as case:
            # 2.3.4. Right click menu on template > modify template > PiP Designer
            # open PiP designer
            pip_room_page.select_specific_tag('All Content')
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_ModifyTemplate('PiP')

            check_result = pip_room_page.check_in_PiP_designer()
            case.result = check_result

            # leave pip designer
            pip_room_page.press_esc_key()

        with uuid('42dacc74-61b9-4492-ad5a-800f61277c9a') as case:
            # 2.3.4. Right click menu on template > modify template > Mask Designer
            # open mask designer
            pip_room_page.hover_library_media('Dialog_03')
            check_result = pip_room_page.select_RightClickMenu_ModifyTemplate('Mask')
            case.result = check_result

            # leave pip designer
            pip_room_page.press_esc_key()

        # with uuid('0a037d50-32d7-48ae-a8c0-963b23a465b0') as case:
        #     # 2.3.4. Right click menu on template > share and update to internet
        #     # open upload dialog
        #     # pip_room_page.hover_library_media('001_lake')
        #     # pip_room_page.select_RightClickMenu_ShareUploadToInternet()
        #     # waiting for create custom pip object page function ready
        #     case.result = None

        with uuid('5d577eca-adaa-4dfc-bef6-8d7843d49d10') as case:
            # 2.3.4. Right click menu on template > delete(only for custom/downloaded)
            # remove selected template
            pip_room_page.select_specific_tag('Downloaded')
            pip_room_page.click_ImportPiPObject(Test_Material_Folder + '2144330281-1615752299605.dzp')
            time.sleep(DELAY_TIME * 3)
            pip_room_page.click_OK_onEffectExtractor()
            pip_room_page.hover_library_media('Frame5317')
            check_result = pip_room_page.select_RightClickMenu_Delete()
            case.result = check_result

        with uuid('5efa0779-a7f7-43c7-995b-7b5a8b874d30') as case:
            # 2.3.4. Right click menu on template > add to > custom tags
            # add template to custom tag
            pip_room_page.add_new_tag('New Tag')
            pip_room_page.select_specific_tag('All Content')
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_Addto('New Tag')

            pip_room_page.select_specific_tag('New Tag')
            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_3_4_3.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_3_4_3.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('b34e9dab-c129-4c03-ade3-0856b8de4602') as case:
            # 2.3.4. Right click menu on template > dock/undock library window
            # dock/undock library window
            pip_room_page.hover_library_media('Dialog_03')
            pip_room_page.select_RightClickMenu_DockUndock_LibraryWindow()

            image_full_path = Auto_Ground_Truth_Folder + 'pip_room_2_3_4_4.png'
            ground_truth = Ground_Truth_Folder + 'pip_room_2_3_4_4.png'
            current_preview = pip_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)

            check_result = pip_room_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    38c5be55-4818-4432-8304-03fa5ae296d3
                    b1a6c212-e2de-46be-9cc6-0c6003cc5847
                    f73e33fa-aab9-49f7-8c97-7a807c426a8b
                    891564d5-777b-45b4-ba74-cadf54b863a2
                    82115509-c6a4-446c-8c12-767138357da4
                    d786486c-9449-4a49-87c8-9c740d8d0536
                    41f874f4-243e-445f-9912-126133a2784b
                    e0a563c7-8ce8-4924-a0d6-1517dfc0c405
                    8ae1a7b5-ca99-4029-87c8-b13e28f13f7c
                    f5c27fc9-99b7-440d-abcd-d8187d961c7c
                    0a037d50-32d7-48ae-a8c0-963b23a465b0
                    7db4eefd-96c9-49cb-b62f-18e7c76858a2
                    59bd1ed2-5bf5-4f24-85a2-e501e0998165
                    0ce6b9b8-f24d-4b26-8876-a4f5a1945294
                    871f45e7-d3eb-454d-b07c-10731492fd82
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'
