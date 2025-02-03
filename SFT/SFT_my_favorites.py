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
base_page = PageFactory().get_page_object('base_page', mwc)
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)
timeline_page = PageFactory().get_page_object('timeline_operation_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page',mwc)
project_room_page = PageFactory().get_page_object('project_room_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
effect_room_page = PageFactory().get_page_object('effect_room_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
transition_room_page = PageFactory().get_page_object('transition_room_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page', mwc)

# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="My Favorites.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder - Setup for Overall Project
Ground_Truth_Folder = app.ground_truth_root + '/My_Favorites/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/My_Favorites/'
Test_Material_Folder = app.testing_material

# For Ground Truth / Test Material folder - Setup for Duncan personal testing
# Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/GroundTruth/Title_Room/'
# Auto_Ground_Truth_Folder = '/Users/cl/Desktop/Duncan/SFT/ATGroundTruth/Title_Room/'
# Test_Material_Folder = '/Users/cl/Desktop/Duncan/Material/'

DELAY_TIME = 1

class Test_My_Favorites():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(DELAY_TIME*4)
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
            google_sheet_execution_log_init('My_Favorites')

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

    @pytest.mark.skip
    def test_1_1_1(self):
        with uuid("89d70e54-7063-4cf7-98d7-02c4a7d27536") as case:
            # Enter Project Room > Check My Favorites...
            main_page.set_project_aspect_ratio_16_9()
            time.sleep(1)
            project_room_page.enter_project_room()

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L7_ProjectRoom_MyFavorites.png', is_project_room=1)
            compare_result = main_page.compare(Ground_Truth_Folder + 'L7_ProjectRoom_MyFavorites.png', current_image)
            case.result = compare_result
    """
    def test_1_1_10(self):
        #Able to select project to import
        with uuid("6b7f015b-4b88-447f-a6cc-6106b4d28efd") as case:
            project_room_page.enter_project_room()
            project_room_page.import_pds_project(app.testing_material + 'My_Favorites/test.pds/')
            if main_page.exist({'AXIdentifier': 'IDD_CLALERT'}):
                main_page.handle_merge_media_to_current_library_dialog()
            time.sleep(2)
            project_room_page.enter_project_room()
            project_room_page.select_LibraryRoom_category('My Projects')
            main_page.select_library_icon_view_media('test')

            # Right click > Add to "My Favorites"...
            time.sleep(1)
            main_page.click_template_its_heart_icon('test')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L10_ProjectRoom_AddTo_MyFavorites_ContextMenu.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L10_ProjectRoom_AddTo_MyFavorites_ContextMenu.png', current_image)

            time.sleep(1)
            # Check "My favorites" > "Arrow 2" effect
            transition_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('test')
            case.result = check_result and compare_result
    """

    @exception_screenshot
    def test_1_1_2(self):
        with uuid("0397c0f3-3898-487f-b3e2-ff03e88fe566") as case:
            # Enter Title Room > Check My Favorites...
            main_page.enter_room(1)

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L26_TitleRoom_MyFavorites.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L26_TitleRoom_MyFavorites.png', current_image)
            case.result = compare_result


        with uuid("9b11f304-f5f2-4ee9-901a-f70ab5ca4f82") as case:
            # Enter Title Room > Right click > Add to "My Favorites"...

            time.sleep(1)
            # Enter "All Content" > "Clover_03" effect
            title_room_page.select_LibraryRoom_category('General')
            time.sleep(1)
            main_page.select_library_icon_view_media('Clover_03')

            # Add to "My Favorites"...
            time.sleep(1)
            main_page.right_click()
            time.sleep(1)
            main_page.select_right_click_menu('Add to', 'My Favorites')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L31_TitleRoom_AddTo_MyFavorites_ContextMenu.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L31_TitleRoom_AddTo_MyFavorites_ContextMenu.png', current_image)

            time.sleep(1)
            # Check "My favorites" > "Clover_03" effect
            title_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Clover_03')
            case.result = check_result and compare_result


        with uuid("e203d7b6-0312-452b-9512-61333cae12d1") as case:
            # Enter Title Room > Right click > Add to "Remove from My Favorites"

            # Right click > "Remove from My Favorites"
            time.sleep(1)
            main_page.right_click()
            time.sleep(1)
            test = main_page.select_right_click_menu('Remove from My Favorites')
            logger(test)

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L38_TitleRoom_Removefrom_LeftPanel_Empty_MyFavorites.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L38_TitleRoom_Removefrom_LeftPanel_Empty_MyFavorites.png', current_image)

            # Snapshot "My favorites" category of Title Room
            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L38_TitleRoom_Removefrom_Library_Empty_MyFavorites.png'
            ground_truth = Ground_Truth_Folder + 'L38_TitleRoom_Removefrom_Library_Empty_MyFavorites.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.library, file_name=image_full_path)
            logger (current_preview)
            case.result = main_page.compare(ground_truth, current_preview) and compare_result


        with uuid("6f9b1dbf-7a07-44b1-b627-d6bcbb62cd15") as case:
            # Enter Title Room > Right click > "Add to" + "Remove from" + "Add to My Favorites"

            # Select Template
            time.sleep(1)
            title_room_page.select_LibraryRoom_category('General')
            main_page.select_library_icon_view_media('Clover_01')

            # Add to "My Favorites"
            time.sleep(1)
            main_page.right_click()
            time.sleep(1)
            main_page.select_right_click_menu('Add to', 'My Favorites')
            time.sleep(1)
            main_page.select_library_icon_view_media('Clover_01')
            main_page.right_click()
            main_page.select_right_click_menu('Remove from My Favorites')
            time.sleep(1)
            main_page.select_library_icon_view_media('Clover_01')
            main_page.right_click()
            main_page.select_right_click_menu('Add to', 'My Favorites')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L48_TitleRoom_Add-Remove-Add_MyFavorites_ContextMenu.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L48_TitleRoom_Add-Remove-Add_MyFavorites_ContextMenu.png', current_image)

            time.sleep(3)
            # Check "My favorites" > "Clover_01" effect
            title_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Clover_01')
            case.result = check_result and compare_result

    def test_1_1_3(self):
        with uuid("97d7a5e0-c954-4ac0-acd9-5aa17d4ef683") as case:
            # Title Room > click Heart icon > Add to "My Favorites"...
            main_page.enter_room(1)
            time.sleep(1)

            # Enter "All Content" > "Clover_01" effect
            pip_room_page.select_LibraryRoom_category('General')
            main_page.select_library_icon_view_media('Clover_01')

            # click Heart icon > Add to "My Favorites"...
            time.sleep(1)
            main_page.click_template_its_heart_icon('Clover_01')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L29_TitleRoom_AddTo_MyFavorites_HeartIcon.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L29_TitleRoom_AddTo_MyFavorites_HeartIcon.png', current_image)

            time.sleep(1)
            # Check "My favorites" > "Clover_01" effect
            title_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Clover_01')
            case.result = check_result and compare_result

        with uuid("4e89aa54-7cb7-40c6-a279-5d8e0aeface8") as case:
            # Keep "My favorites" > click Heart icon > Remove from "My Favorites"...

            # Select "Clover_01" effect
            main_page.select_library_icon_view_media('Clover_01')

            #Remove from "My Favorites"...
            time.sleep(1)
            main_page.click_template_its_heart_icon('Clover_01')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L35_TitleRoom_Remove_MyFavorites_HeartIcon.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L35_TitleRoom_Remove_MyFavorites_HeartIcon.png', current_image)

            case.result = compare_result


    def test_1_1_4(self):
        with uuid("913b4f15-b7c8-4413-a96b-36ff348b2db4") as case:
            # Enter Transition Room > Check My Favorites...
            main_page.enter_room(2)

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L48_TransitionRoom_MyFavorites.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L48_TransitionRoom_MyFavorites.png', current_image)
            case.result = compare_result


        with uuid("3a6b63ec-9e58-4723-b5e9-823ee16f0a00") as case:
            # Enter Transition Room > Right click > Add to "My Favorites"...

            time.sleep(1)
            # Enter "All Content" > "Arrow 2" effect
            transition_room_page.select_LibraryRoom_category('All Content')
            main_page.select_library_icon_view_media('Arrow 2')


            # Right click > Add to "My Favorites"...
            time.sleep(1)
            main_page.right_click()
            time.sleep(1)
            main_page.select_right_click_menu('Add to', 'My Favorites')


            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L55_TransitionRoom_AddTo_MyFavorites_ContextMenu.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L55_TransitionRoom_AddTo_MyFavorites_ContextMenu.png', current_image)

            time.sleep(1)
            # Check "My favorites" > "Arrow 2" effect
            transition_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Arrow 2')
            case.result = check_result and compare_result




        with uuid("c92e8bf4-82cc-4237-8193-c4c975be7369") as case:
            # Enter Transition Room > Right click > Add to "Remove from My Favorites"

            # Right click > "Remove from My Favorites"
            time.sleep(1)
            main_page.right_click()
            time.sleep(1)
            main_page.select_right_click_menu('Remove from My Favorites')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(
                file_name=Auto_Ground_Truth_Folder + 'L62_TransitionRoom_Removefrom_LeftPanel_Empty_MyFavorites.png')
            compare_result = main_page.compare(
                Ground_Truth_Folder + 'L62_TransitionRoom_Removefrom_LeftPanel_Empty_MyFavorites.png', current_image)

            # Snapshot "My favorites" category of Title Room
            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L62_TransitionRoom_Removefrom_Library_Empty_MyFavorites.png'
            ground_truth = Ground_Truth_Folder + 'L62_TransitionRoom_Removefrom_Library_Empty_MyFavorites.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.library, file_name=image_full_path)
            logger(current_preview)
            case.result = main_page.compare(ground_truth, current_preview) and compare_result

        with uuid("43101dfe-f6e3-49ab-8269-c487e390e2c8") as case:
            # Enter Transition Room > Right click > "Add to" + "Remove from" + "Add to My Favorites"

            # Select Template
            time.sleep(1)
            title_room_page.select_LibraryRoom_category('All Content')
            main_page.select_library_icon_view_media('Anaglyph')

            # Add to "My Favorites"
            time.sleep(1)
            main_page.right_click()
            time.sleep(1)
            main_page.select_right_click_menu('Add to', 'My Favorites')
            time.sleep(1)
            main_page.select_library_icon_view_media('Anaglyph')
            main_page.right_click()
            main_page.select_right_click_menu('Remove from My Favorites')
            time.sleep(1)
            main_page.select_library_icon_view_media('Anaglyph')
            main_page.right_click()
            main_page.select_right_click_menu('Add to', 'My Favorites')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L69_TransitionRoom_Add-Remove-Add_MyFavorites_ContextMenu.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L69_TransitionRoom_Add-Remove-Add_MyFavorites_ContextMenu.png', current_image)

            time.sleep(1)
            # Check "My favorites" > "Back Light" effect
            transition_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Anaglyph')
            case.result = check_result and compare_result

    def test_1_1_5(self):
        with uuid("db84322c-2b50-41c3-9011-31980c0a3045") as case:
            # Enter Transition Room > click Heart icon > Add to "My Favorites"...
            main_page.enter_room(2)

            time.sleep(1)
            # Enter "All Content" > "Anaglyph" effect
            transition_room_page.select_LibraryRoom_category('All Content')
            main_page.select_library_icon_view_media('Anaglyph')

            # Add to "My Favorites"...
            time.sleep(1)
            main_page.click_square_template_its_heart_icon('Anaglyph')

            # Check "My favorites"
            transition_room_page.select_LibraryRoom_category('My Favorites')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L53_TransitionRoom_AddTo_MyFavorites_HeartIcon.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L53_TransitionRoom_AddTo_MyFavorites_HeartIcon.png', current_image)

            time.sleep(1)
            # Check "My favorites" > "Anaglyph" effect
            transition_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Anaglyph')
            case.result = check_result and compare_result

        with uuid("c895b4da-7187-4b88-ba62-f0b5513eef14") as case:
            # Select "My favorites" > click Heart icon > Remove from "My Favorites"...
            main_page.select_library_icon_view_media('Anaglyph')

            # click Heart icon > Remove from "My Favorites"...
            time.sleep(1)
            main_page.click_square_template_its_heart_icon('Anaglyph')


            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L59_TransitionRoom_Removefrom_MyFavorites_HeartIcon.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L59_TransitionRoom_Removefrom_MyFavorites_HeartIcon.png', current_image)

            case.result = compare_result

    def test_1_1_6(self):
        with uuid("64afd18b-771f-4c27-81ae-1595e63f2de1") as case:
            # Enter Effect Room > Check My Favorites...
            main_page.enter_room(3)

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L75_EffectRoom_MyFavorites.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L75_EffectRoom_MyFavorites.png', current_image)
            case.result = compare_result

        with uuid("c4131247-4ad0-4492-8cff-99463d961f9f") as case:
            # Enter Effect Room > Right click > Add to "My Favorites"...

            time.sleep(1)
            # Enter "All Content" > "Aberration" effect
            effect_room_page.select_LibraryRoom_category('All Content')
            main_page.select_library_icon_view_media('Aberration')

            # Right click > Add to "My Favorites"...
            time.sleep(1)
            main_page.right_click()
            time.sleep(1)
            main_page.select_right_click_menu('Add to', 'My Favorites')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L81_EffectRoom_AddTo_MyFavorites_ContextMenu.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L81_EffectRoom_AddTo_MyFavorites_ContextMenu.png', current_image)

            time.sleep(1)
            # Check "My favorites" > "Aberration" effect
            effect_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Aberration')
            case.result = check_result and compare_result

        """
            effect_room_page.select_LibraryRoom_category('123')
            main_page.select_library_icon_view_media('LUT_Cinespace')
            check_result = effect_room_page.remove_from_custom_tag(4,
                                                                   'LUT_Cinespace')  # The tag_index of 'My Favorite' is 0
            logger(check_result)
        """

        with uuid("dab85e3d-c07a-404b-a42a-d5f0e87a4134") as case:
            # Enter Effect Room > Right click > Add to "Remove from My Favorites"

            # Right click > "Remove from My Favorites"
            time.sleep(1)
            main_page.right_click()
            time.sleep(1)
            main_page.select_right_click_menu('Remove from My Favorites')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(
                file_name=Auto_Ground_Truth_Folder + 'L88_EffectRoom_Removefrom_LeftPanel_Empty_MyFavorites.png')
            compare_result = main_page.compare(
                Ground_Truth_Folder + 'L88_EffectRoom_Removefrom_LeftPanel_Empty_MyFavorites.png', current_image)

            # Snapshot "My favorites" category of Effect Room
            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L88_EffectRoom_Removefrom_Library_Empty_MyFavorites.png'
            ground_truth = Ground_Truth_Folder + 'L88_EffectRoom_Removefrom_Library_Empty_MyFavorites.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.library, file_name=image_full_path)
            logger(current_preview)
            case.result = main_page.compare(ground_truth, current_preview) and compare_result


        with uuid("471c1971-52b6-4016-b933-85966c4263d6") as case:
            # Enter Effect Room > Right click > "Add to" + "Remove from" + "Add to My Favorites"

            # Select Template
            time.sleep(1)
            title_room_page.select_LibraryRoom_category('All Content')
            main_page.select_library_icon_view_media('Back Light')

            # Add to "My Favorites"
            time.sleep(1)
            main_page.right_click()
            time.sleep(3)
            main_page.select_right_click_menu('Add to', 'My Favorites')
            time.sleep(1)
            main_page.select_library_icon_view_media('Back Light')
            main_page.right_click()
            main_page.select_right_click_menu('Remove from My Favorites')
            time.sleep(1)
            main_page.select_library_icon_view_media('Back Light')
            main_page.right_click()
            main_page.select_right_click_menu('Add to', 'My Favorites')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L96_EffectRoom_Add-Remove-Add_MyFavorites_ContextMenu.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L96_EffectRoom_Add-Remove-Add_MyFavorites_ContextMenu.png', current_image)

            time.sleep(1)
            # Check "My favorites" > "Back Light" effect
            effect_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Back Light')
            case.result = check_result and compare_result

    def test_1_1_7(self):
        with uuid("bc856fbc-8b26-4ca0-b595-3c972cd8fa22") as case:
            # Enter Effect Room > click Heart icon > Add to "My Favorites"...
            main_page.enter_room(3)
            time.sleep(1)

            # Enter "All Content" > "Aberration" effect
            effect_room_page.select_LibraryRoom_category('All Content')
            main_page.select_library_icon_view_media('Aberration')

            # click Heart icon > Add to "My Favorites"...
            time.sleep(1)
            main_page.click_square_template_its_heart_icon('Aberration')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L82_EffectRoom_AddTo_MyFavorites_HeartIcon.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L82_EffectRoom_AddTo_MyFavorites_HeartIcon.png', current_image)

            time.sleep(1)
            # Check "My favorites" > "Aberration" effect
            effect_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Aberration')
            case.result = check_result and compare_result


        with uuid("2df8e147-ec54-4ab3-8bbc-669fae69660f") as case:
            # Enter Effect Room > click Heart icon > Remove from "My Favorites"...
            time.sleep(1)

            # Enter "All Content" > "Aberration" effect
            main_page.select_library_icon_view_media('Aberration')

            # click Heart icon > Remove from "My Favorites"...
            time.sleep(1)
            main_page.click_square_template_its_heart_icon('Aberration')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L85_EffectRoom_Removefrom_MyFavorites_HeartIcon.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L85_EffectRoom_Removefrom_MyFavorites_HeartIcon.png', current_image)

            case.result = compare_result

    def test_1_1_8(self):
        with uuid("a7207805-22dd-4088-8707-f842ed4df2dc") as case:
            # Enter PiP Room > Check My Favorites...
            main_page.enter_room(4)

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L92_PiPRoom_MyFavorites.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L92_PiPRoom_MyFavorites.png', current_image)
            case.result = compare_result

        with uuid("27e321c1-17b3-48c9-9fa1-448780eacf0d") as case:
            # PiP Room > Right click > Add to "My Favorites"...

            time.sleep(1)
            # Enter "All Content" > "Dialog_04" effect
            pip_room_page.select_LibraryRoom_category('General')
            main_page.select_library_icon_view_media('Dialog_04')

            # Right click > Add to "My Favorites"...
            time.sleep(1)
            main_page.right_click()
            time.sleep(1)
            main_page.select_right_click_menu('Add to', 'My Favorites')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L103_PiPRoom_AddTo_MyFavorites_ContextMenu.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L103_PiPRoom_AddTo_MyFavorites_ContextMenu.png', current_image)

            time.sleep(1)
            # Check "My favorites" > "Dialog_04" effect
            pip_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Dialog_04')
            case.result = check_result and compare_result



        with uuid("9792ac59-1db0-4005-89b6-d3448341a8c0") as case:
            # Enter PiP Room > Right click > Add to "Remove from My Favorites"

            # Right click > "Remove from My Favorites"
            time.sleep(1)
            main_page.right_click()
            time.sleep(1)
            main_page.select_right_click_menu('Remove from My Favorites')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(
                file_name=Auto_Ground_Truth_Folder + 'L110_PiPRoom_Removefrom_LeftPanel_Empty_MyFavorites.png')
            compare_result = main_page.compare(
                Ground_Truth_Folder + 'L110_PiPRoom_Removefrom_LeftPanel_Empty_MyFavorites.png', current_image)

            # Snapshot "My favorites" category of PiP Room
            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L110_PiPRoom_Removefrom_Library_Empty_MyFavorites.png'
            ground_truth = Ground_Truth_Folder + 'L110_PiPRoom_Removefrom_Library_Empty_MyFavorites.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.library, file_name=image_full_path)
            logger(current_preview)
            case.result = main_page.compare(ground_truth, current_preview) and compare_result

        with uuid("40a26912-0055-4caf-b924-b6783984b5c3") as case:
            # Enter PiP Room > Right click > "Add to" + "Remove from" + "Add to My Favorites"

            # Select Template
            time.sleep(1)
            title_room_page.select_LibraryRoom_category('General')
            main_page.select_library_icon_view_media('Dialog_06')

            # Add to "My Favorites"
            time.sleep(1)
            main_page.right_click()
            time.sleep(1)
            main_page.select_right_click_menu('Add to', 'My Favorites')
            time.sleep(1)
            main_page.select_library_icon_view_media('Dialog_06')
            main_page.right_click()
            main_page.select_right_click_menu('Remove from My Favorites')
            time.sleep(1)
            main_page.select_library_icon_view_media('Dialog_06')
            main_page.right_click()
            main_page.select_right_click_menu('Add to', 'My Favorites')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L120_PiPRoom_Add-Remove-Add_MyFavorites_ContextMenu.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L120_PiPRoom_Add-Remove-Add_MyFavorites_ContextMenu.png', current_image)

            time.sleep(1)
            # Check "My favorites" > "Dialog_06" effect
            pip_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Dialog_06')
            case.result = check_result and compare_result

    def test_1_1_9(self):
        with uuid("e00e7a56-e87d-4b94-8541-c810c874f4ff") as case:
            # PiP Room > click Heart icon > Add to "My Favorites"...
            main_page.enter_room(4)
            time.sleep(1)

            # Enter "All Content" > "Dialog_04" effect
            title_room_page.select_LibraryRoom_category('General')
            main_page.select_library_icon_view_media('Dialog_04')

            # click Heart icon > Add to "My Favorites"...
            time.sleep(1)
            main_page.click_template_its_heart_icon('Dialog_04')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L101_PiPRoom_AddTo_MyFavorites_HeartIcon.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L101_PiPRoom_AddTo_MyFavorites_HeartIcon.png', current_image)

            time.sleep(1)
            # Check "My favorites" > "Dialog_04" effect
            pip_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Dialog_04')
            case.result = check_result and compare_result


        with uuid("24b7e58c-a74e-458e-8062-40609a7482fa") as case:
            # Keep "My Favorites" > click Heart icon > Remove "My Favorites"...
            time.sleep(1)

            # Enter "All Content" > "Dialog_04" effect
            main_page.select_library_icon_view_media('Dialog_04')

            # click Heart icon > Remove from "My Favorites"...
            time.sleep(1)
            main_page.click_template_its_heart_icon('Dialog_04')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L107_PiPRoom_Removefrom_MyFavorites_HeartIcon.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L107_PiPRoom_Removefrom_MyFavorites_HeartIcon.png', current_image)

            time.sleep(1)
            # Check "My favorites" > "Dialog_04" effect
            pip_room_page.select_LibraryRoom_category('My Favorites')
            case.result = compare_result


    @exception_screenshot
    def test_1_1_10(self):
        with uuid("c76055fe-ffda-4aa1-8f93-1951e0633ef4") as case:
            # Enter Particle Room > Check My Favorites...
            main_page.enter_room(5)

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L114_ParticleRoom_MyFavorites.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L114_ParticleRoom_MyFavorites.png', current_image)
            case.result = compare_result


        with uuid("92506591-c433-47a1-ab87-0cd402debda9") as case:
            # Enter Particle Room > Right click > Add to "My Favorites"...

            time.sleep(1)
            # Enter "All Content" > "Maple" effect
            particle_room_page.select_LibraryRoom_category('General')
            main_page.select_library_icon_view_media('Maple')

            # Right click > Add to "My Favorites"...
            time.sleep(1)
            main_page.right_click()
            time.sleep(1)
            main_page.select_right_click_menu('Add to', 'My Favorites')


            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L126_TitleRoom_AddTo_MyFavorites_ContextMenu.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L126_TitleRoom_AddTo_MyFavorites_ContextMenu.png', current_image)


            time.sleep(1)
            # Check "My favorites" > "Maple" effect
            particle_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Maple')
            case.result = check_result and compare_result

        with uuid("ff503957-b367-4a16-a508-dafd820bec51") as case:
            # Enter Particle Room > Right click > Add to "Remove from My Favorites"

            # Right click > "Remove from My Favorites"
            time.sleep(1)
            main_page.right_click()
            time.sleep(1)
            main_page.select_right_click_menu('Remove from My Favorites')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(
                file_name=Auto_Ground_Truth_Folder + 'L133_ParticleRoom_Removefrom_LeftPanel_Empty_MyFavorites.png')
            compare_result = main_page.compare(
                Ground_Truth_Folder + 'L133_ParticleRoom_Removefrom_LeftPanel_Empty_MyFavorites.png', current_image)

            # Snapshot "My favorites" category of Title Room
            time.sleep(1)
            image_full_path = Auto_Ground_Truth_Folder + 'L133_ParticleRoom_Removefrom_Library_Empty_MyFavorites.png'
            ground_truth = Ground_Truth_Folder + 'L133_ParticleRoom_Removefrom_Library_Empty_MyFavorites.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.library, file_name=image_full_path)
            logger(current_preview)
            case.result = main_page.compare(ground_truth, current_preview) and compare_result

        with uuid("008ec4ab-ca83-40b9-b4ba-a95c4bedb01c") as case:
            # Enter Particle Room > Right click > "Add to" + "Remove from" + "Add to My Favorites"

            # Select Template
            time.sleep(1)
            title_room_page.select_LibraryRoom_category('General')
            main_page.select_library_icon_view_media('Maple')

            # Add to "My Favorites"
            time.sleep(1)
            main_page.right_click()
            time.sleep(1)
            main_page.select_right_click_menu('Add to', 'My Favorites')
            time.sleep(1)
            main_page.select_library_icon_view_media('Maple')
            main_page.right_click()
            main_page.select_right_click_menu('Remove from My Favorites')
            time.sleep(1)
            main_page.select_library_icon_view_media('Maple')
            main_page.right_click()
            main_page.select_right_click_menu('Add to', 'My Favorites')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L143_ParticleRoom_Add-Remove-Add_MyFavorites_ContextMenu.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L143_ParticleRoom_Add-Remove-Add_MyFavorites_ContextMenu.png', current_image)

            time.sleep(1)
            # Check "My favorites" > "Maple" effect
            particle_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Maple')
            case.result = check_result and compare_result

    def test_1_1_11(self):
        with uuid("e00e7a56-e87d-4b94-8541-c810c874f4ff") as case:
            # Particle Room > click Heart icon > Add to "My Favorites"...
            main_page.enter_room(5)
            time.sleep(1)

            # Enter "All Content" > "Dialog_04" effect
            pip_room_page.select_LibraryRoom_category('General')
            main_page.select_library_icon_view_media('Maple')

            # click Heart icon > Add to "My Favorites"...
            time.sleep(1)
            main_page.click_template_its_heart_icon('Maple')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L124_ParticleRoom_AddTo_MyFavorites_HeartIcon.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L124_ParticleRoom_AddTo_MyFavorites_HeartIcon.png', current_image)

            time.sleep(1)
            # Check "My favorites" > "Maple" effect
            particle_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Maple')
            case.result = check_result and compare_result

        with uuid("c7365c23-e1f3-4ab3-80b7-7741b7793dd4") as case:
            # Keep "My Favorites" > click Heart icon > Remove from "My Favorites"...

            # Select "Maple" effect
            main_page.select_library_icon_view_media('Maple')

            # click Heart icon > Remove from "My Favorites"...
            time.sleep(1)
            main_page.click_template_its_heart_icon('Maple')

            time.sleep(1)
            # Snapshot "My favorites" of left_panel
            current_image = main_page.snapshot_my_favorites_left_panel(file_name=Auto_Ground_Truth_Folder + 'L130_ParticleRoom_Removefrom_MyFavorites_HeartIcon.png')
            compare_result = main_page.compare(Ground_Truth_Folder + 'L130_ParticleRoom_Removefrom_MyFavorites_HeartIcon.png', current_image)

            case.result = compare_result



