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
transition_room_page = PageFactory().get_page_object('transition_room_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Transition Room.html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Transition_Room/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Transition_Room/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1

# @pytest.fixture(scope="module", autouse= True)
# def init():
#     yield
#     main_page.close_app()
#     report.export()
#     report.show()

class Test_Transition_Room():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        time.sleep(3)
        main_page.insert_media("Food.jpg")
        main_page.select_library_icon_view_media("Landscape 01.jpg")
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media("Skateboard 01.mp4")
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media("Skateboard 02.mp4")
        main_page.tips_area_insert_media_to_selected_track(option=1)

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
            google_sheet_execution_log_init('Transition_Room')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"transition room result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        with uuid("a2d7a03e-0e64-4ef5-b41a-cb7f1abd452b") as case:
            # Insert Food.jpg/Landscape 01.jpg/Skateboard 01.mp4/Skateboard 02.mp4 > Enter Transition Room
            time.sleep(DELAY_TIME)
            # 1.1.1. Mouse click enter Transition Room
            main_page.enter_room(2)

            SetCheck_result = L.transition_room.explore_view_region.table_all_content_tags

            if not transition_room_page.exist(locator=SetCheck_result):
                case.result = False
            else:
                case.result = True
            main_page.enter_room(0)

        with uuid("3d165a49-9f15-441d-91a9-67a920db991e") as case:
            # 1.1.3. Hotkey enter (F8)
            time.sleep(DELAY_TIME)
            transition_room_page.tap_TransitionRoom_hotkey()
            # with transition_room_page.keyboard.pressed(main_page.keyboard.key.f8):
            #     pass
            SetCheck_result = L.transition_room.explore_view_region.table_all_content_tags

            if not transition_room_page.exist(locator=SetCheck_result):
                case.result = False
            else:
                case.result = True

            time.sleep(DELAY_TIME)

        with uuid("14eec8ff-7c5c-477f-8f6e-770395232e53") as case:
            # 2.1.1. Import Media - Import Transition Objects
            time.sleep(DELAY_TIME)
            transition_room_page.\
                click_ImportTransitionTemplates(Test_Material_Folder + '1730581156-1614204308302.dztr')
            time.sleep(DELAY_TIME)
            transition_room_page.click_OK_onEffectExtractor()
            # check import process success
            SetCheck_result = \
                transition_room_page.check_is_in_special_category('Downloaded', 'Transition Moneda Bitcoin')

            if not SetCheck_result:
                case.result = False
            else:
                case.result = True

            time.sleep(DELAY_TIME)

        with uuid('604e940a-4a7a-4ee1-8c99-319f61a36657') as case:
            # 2.1.1. Import Media - Log in to CL Cloud to download Transition templates
            transition_room_page.download_content_from_CL('01-Rings')
            time.sleep(DELAY_TIME*4)

            # check import process success
            SetCheck_result = transition_room_page.check_is_in_special_category('Downloaded', '01-Rings')

            if not SetCheck_result:
                case.result = False
            else:
                case.result = True

        with uuid('af67f00b-8b4b-464d-b8f3-3cacc1b89c2d') as case:
            # 2.3.3. Right click menu on template > delete import transition template
            check_result_1 = transition_room_page.delete_content_in_Download_category('Transition Moneda Bitcoin')
            check_result_2 = transition_room_page.delete_content_in_Download_category('01-Rings')

            case.result = check_result_1 and check_result_2

        with uuid('4677a996-2507-46f8-a957-6ce6d8f5e379') as case:
            # 2.1.3. Select Category, content match the selected category
            check_result_1 = transition_room_page.check_is_in_special_category('General', 'Fade')
            check_result_2 = transition_room_page.check_is_in_special_category('Special', 'Burning')
            check_result_3 = transition_room_page.check_is_in_special_category('3D/3D-Like', 'Magic Blocks')
            check_result_4 = transition_room_page.check_is_in_special_category('Alpha', 'Binary 1')
            check_result_5 = transition_room_page.check_is_in_special_category('Block', 'Blizzard')
            check_result = check_result_1 and check_result_2 and check_result_3 and check_result_4 and check_result_5
            if not check_result:
                case.result = False
            else:
                case.result = True

        with uuid('2823048d-5056-4996-bc16-916c24886afd') as case:
            # 2.1.6. Details view
            # transition_room_page.select_LibraryRoom_category('All Content')
            # main_page.tap_Library_DetailView()
            check_result = main_page.click_library_details_view()
            if not check_result:
                case.result = False
            else:
                case.result = True

        with uuid('9555f8a6-488f-4cdc-8aef-185c9b53298d') as case:
            # 2.1.7. icon view
            # main_page.tap_Library_IconView()
            check_result = main_page.click_library_icon_view()
            if not check_result:
                case.result = False
            else:
                case.result = True

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        with uuid('60ef5ad6-88a7-46f1-84e9-90881e00f440') as case:
            # 2.3.3. Right click menu on template > Add to My Favorites
            # Add some transitions to My Favorite
            transition_room_page.tap_TransitionRoom_hotkey()
            transition_room_page.select_LibraryRoom_category('All Content')
            main_page.select_library_icon_view_media('Arrow 2')
            transition_room_page.select_RightClickMenu_Addto('My Favorites')
            time.sleep(DELAY_TIME)

            transition_room_page.select_LibraryRoom_category('My Favorites')
            check_result = main_page.select_library_icon_view_media('Arrow 2')
            case.result = check_result

        with uuid('d0019a59-7886-4794-8254-660963f1a987') as case:
            # 2.4.1. Library Menu > Apply My Favorite Transition to All Videos > With any clip on timeline
            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)
            time.sleep(DELAY_TIME)
            check_result = transition_room_page.exist_click(L.media_room.library_menu.btn_menu)
            case.result = check_result

        with uuid('b9386b44-d42a-4857-b0fc-a4086eacae59') as case:
            # 2.1.8. Library menu > Apply my favorite Transition to all videos
            # apply to all video - Prefix
            time.sleep(DELAY_TIME)

            transition_room_page.apply_LibraryMenu_MyFavorite_Transition_to_all_video('Prefix')
            main_page.set_timeline_timecode('00_00_01_08')

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_1.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_1.png'
            current_preview = transition_room_page.snapshot(
                locator=L.playback_window.main, file_name=image_full_path)
            check_result_1 = transition_room_page.compare(ground_truth, current_preview)

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_2.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_2.png'
            current_preview = transition_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result_2 = transition_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('0838e59b-d60c-4630-9232-574a046f4259') as case:
            # 2.1.8. Library menu > Apply my favorite Transition to all videos
            # apply to all video - Postfix
            transition_room_page.apply_LibraryMenu_MyFavorite_Transition_to_all_video('Postfix')

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_3.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_3.png'
            current_preview = transition_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('c768a55d-249e-4fa4-95bd-7ebc3d359418') as case:
            # 2.1.8. Library menu > Apply my favorite Transition to all videos
            # apply to all video - Cross
            transition_room_page.apply_LibraryMenu_MyFavorite_Transition_to_all_video('Cross')

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_4.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_4.png'
            current_preview = transition_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

            # undo
            with transition_room_page.keyboard.pressed(main_page.keyboard.key.cmd, 'z'):
                pass

        with uuid('83997972-efc6-4129-914a-79380e564525') as case:
            # 2.1.8. Library menu > Apply my favorite Transition to all videos
            # apply to all video - Overlap
            transition_room_page.apply_LibraryMenu_MyFavorite_Transition_to_all_video('Overlap')

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_5.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_5.png'
            current_preview = transition_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('4fd631f1-bdb1-4714-bfdf-b7e2d747faec') as case:
            # 2.3.3. Right click menu on template > Remove from My Favorites
            # Remove transition from My Favorites
            time.sleep(DELAY_TIME)
            transition_room_page.select_LibraryRoom_category('My Favorites')
            main_page.select_library_icon_view_media('Arrow 2')
            transition_room_page.select_RightClickMenu_RemoveFromFavorites()

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_3_3_1.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_3_3_1.png'
            current_preview = transition_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                            file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('7e0cb745-c141-4243-92de-f2fd7f40146e') as case:
            # 2.4.1. Library Menu > Apply My Favorite Transition to All Videos > Empty track
            time.sleep(DELAY_TIME)
            main_page.close_and_restart_app()
            time.sleep(DELAY_TIME * 2)
            transition_room_page.tap_TransitionRoom_hotkey()
            time.sleep(DELAY_TIME)

            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_4_1_2.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_4_1_2.png'
            current_preview = transition_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        with uuid('be77baea-4d9d-4c00-b9ae-9f2f6173e2c6') as case:
            # 2.1.8. Library menu > Apply Fading Transition to all videos
            # apply to all video - Prefix
            transition_room_page.tap_TransitionRoom_hotkey()
            time.sleep(DELAY_TIME)

            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Prefix')

            main_page.set_timeline_timecode('00_00_00_20')

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_6.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_6.png'
            current_preview = transition_room_page.snapshot(
                locator=L.playback_window.main, file_name=image_full_path)
            check_result_1 = transition_room_page.compare(ground_truth, current_preview)

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_7.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_7.png'
            current_preview = transition_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result_2 = transition_room_page.compare(ground_truth, current_preview)

            case.result = check_result_1 and check_result_2

        with uuid('5799041c-0b02-43fa-ad2e-67f1181c214e') as case:
            # 2.1.8. Library menu > Apply Fading Transition to all videos
            # apply to all video - Postfix
            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Postfix')

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_8.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_8.png'
            current_preview = transition_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('6d5b8af2-4634-4e6c-abda-d0b5594f1943') as case:
            # 2.1.8. Library menu > Apply Fading Transition to all videos
            # apply to all video - Cross
            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Cross')

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_9.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_9.png'
            current_preview = transition_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

            # undo
            with transition_room_page.keyboard.pressed(main_page.keyboard.key.cmd, 'z'):
                pass

        with uuid('f48442f4-dc7a-44fb-bb18-8657374202da') as case:
            # 2.1.8. Library menu > Apply Fading Transition to all videos
            # apply to all video - Overlap
            transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Overlap')

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_10.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_10.png'
            current_preview = transition_room_page.snapshot(
                locator=L.timeline_operation.workspace, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        with uuid('18c968b9-483b-491d-8ce8-71c3255ccc10') as case:
            # 2.1.8. Sort by > Sort by Type
            transition_room_page.tap_TransitionRoom_hotkey()
            transition_room_page.sort_by_type()

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_12.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_12.png'
            current_preview = transition_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                            file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('f24299b6-d17b-4c0d-abed-dbbdc282e647') as case:
            # 2.1.8. Sort by > Sort by Name
            transition_room_page.sort_by_name()

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_11.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_11.png'
            current_preview = transition_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                            file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('ef71ac7f-cbe1-4cf0-b006-3e02d4912d7c') as case:
            # 2.1.8. Extra Large Icons > Thumbnails show as extra large icons
            transition_room_page.select_LibraryMenu_ExtraLargeIcons()

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_13.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_13.png'
            current_preview = transition_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                            file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('df61a400-49a9-495b-b58f-ccf00f26d5b4') as case:
            # 2.1.8. Large Icons > Thumbnails show as large icons
            transition_room_page.select_LibraryMenu_LargeIcons()

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_14.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_14.png'
            current_preview = transition_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                            file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('ddbb3acd-86a7-41a0-bf04-ad70b06a01d7') as case:
            # 2.1.8. Medium Icons > Thumbnails show as medium icons
            transition_room_page.select_LibraryMenu_MediumIcons()

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_15.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_15.png'
            current_preview = transition_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                            file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('b6fa22e7-08a6-4bbe-8a49-e5403e0113e6') as case:
            # 2.1.8. Small Icons > Thumbnails show as small icons
            transition_room_page.select_LibraryMenu_SmallIcons()

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_16.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_16.png'
            current_preview = transition_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                            file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

            transition_room_page.select_LibraryMenu_MediumIcons()

        with uuid('3135568b-280f-4403-abb9-6314d332ab50') as case:
            # 2.1.9. Search the library > Show the contents fit the name input in search bar
            transition_room_page.search_Transition_room_library('fade')

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_1_8_17.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_1_8_17.png'
            current_preview = transition_room_page.snapshot(locator=L.media_room.library_listview.main_frame,
                                                            file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

            transition_room_page.search_Transition_room_click_cancel()

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        with uuid("59860f19-5001-4cb7-ab2e-a4e252b53e9f") as case:
            # 2.2. Explorer view
            # 2.2.1. Explorer view > Hide explorer view
            transition_room_page.tap_TransitionRoom_hotkey()

            time.sleep(DELAY_TIME)
            check_result = transition_room_page.click_ExplorerView()
            case.result = check_result

        with uuid("5570ca3a-1797-4342-bafe-570b34f7ee46") as case:
            # 2.2.1. Explorer view > Display explorer view
            time.sleep(DELAY_TIME)
            check_result = transition_room_page.click_ExplorerView()
            case.result = check_result

        with uuid("7fd4cbfd-0eb4-4d34-90cf-2ee639cf4428") as case:
            # 2.2.2. Add a new tag > Set a new name
            time.sleep(DELAY_TIME)
            transition_room_page.add_transitionroom_new_tag('my_new_tag')

            SetCheck_result = transition_room_page.find_specific_tag('my_new_tag')

            if not SetCheck_result:
                case.result = False
            else:
                case.result = True

            transition_room_page.move_mouse_to_0_0()

        with uuid("ac7707be-9db9-4a0c-a52d-b3674861d1d4") as case:
            # 2.2.2. Add a new tag > Set a existed name
            time.sleep(DELAY_TIME)
            check_result = transition_room_page.add_transitionroom_new_tag('my_new_tag')

            if not check_result:
                case.result = True
            else:
                case.result = False

        with uuid("228e7123-f21a-4821-ba54-271c0ba0c32f") as case:
            # 2.2.2. Add a new tag > Set a unicode name
            time.sleep(DELAY_TIME)
            transition_room_page.add_transitionroom_new_tag('許功蓋')

            SetCheck_result = transition_room_page.find_specific_tag('許功蓋')

            if not SetCheck_result:
                case.result = False
            else:
                case.result = True

        with uuid("7bff1406-b0be-4050-ae51-ad9cf68fa7ea") as case:
            # 2.2.3. Delete the selected tag > Default tag
            time.sleep(DELAY_TIME)
            transition_room_page.select_specific_tag('General')
            transition_room_page.right_click()

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_2_3_1.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_2_3_1.png'
            current_preview = transition_room_page.snapshot(
                locator=L.transition_room.explore_view_region.table_all_content_tags, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid("d9413654-4cb3-4a66-8ae6-15767af38842") as case:
            # 2.2.3. Delete the selected tag > Custom tag
            time.sleep(DELAY_TIME)
            transition_room_page.select_tag_RightClickMenu_DeleteTag('my_new_tag')
            check_result = transition_room_page.select_specific_tag('my_new_tag')
            if not check_result:
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        with uuid("e1334dd5-da53-487e-898e-2d5c693cf025") as case:
            # 2.4.5. Multi-clip on timeline > Apply My Favorite Transition to All Videos
            transition_room_page.tap_TransitionRoom_hotkey()
            time.sleep(DELAY_TIME)
            transition_room_page.select_LibraryRoom_category('All Content')
            main_page.select_library_icon_view_media('Arrow 2')
            transition_room_page.select_RightClickMenu_Addto('My Favorites')
            time.sleep(DELAY_TIME)
            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)
            transition_room_page.select_right_click_menu('Apply My Favorite Transition to All Videos')

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_4_5_1.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_4_5_1.png'
            current_preview = transition_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)

            # Remove transition from My Favorites
            transition_room_page.select_LibraryRoom_category('My Favorites')
            main_page.select_library_icon_view_media('Arrow 2')
            transition_room_page.select_RightClickMenu_RemoveFromFavorites()

        with uuid("e36f4055-97e2-4e2f-9fd3-bdff643b58ec") as case:
            # 2.4.5. Multi-clip on timeline > Apply Fading Transition to All Videos
            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)
            transition_room_page.select_right_click_menu('Apply Fading Transition to All Videos')

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_4_5_2.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_4_5_2.png'
            current_preview = transition_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)

        with uuid("ba36567c-0a4c-47ca-9f47-cdfb968965d1") as case:
            # 2.2. Explorer view
            # 2.2.5. Keep tag after re-launch PDR
            # time.sleep(DELAY_TIME * 3)
            main_page.close_and_restart_app()
            time.sleep(DELAY_TIME * 3)
            transition_room_page.tap_TransitionRoom_hotkey()
            time.sleep(DELAY_TIME)
            check_result = transition_room_page.select_specific_tag('許功蓋')
            if not check_result:
                transition_room_page.add_transitionroom_new_tag('許功蓋')
                time.sleep(DELAY_TIME)
                main_page.close_and_restart_app()
                time.sleep(DELAY_TIME * 3)
                transition_room_page.tap_TransitionRoom_hotkey()
                time.sleep(DELAY_TIME)
                if not transition_room_page.select_specific_tag('許功蓋'):
                    case.result = False
                else:
                    case.result = True
            else:
                case.result = True

            time.sleep(DELAY_TIME)

        with uuid("32969540-b5bb-471d-8849-d8e70572440c") as case:
            # 2.4. MISC
            # 2.4.1. Library Menu > Apply My Favorite Transition to All Videos > No Favorite transition object
            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_4_1_1.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_4_1_1.png'
            current_preview = transition_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid("7d5597cf-a9fd-4ca8-a0f0-457884c3cdaf") as case:
            # 2.4.2. Empty Track > Apply Fading Transition to All Videos
            transition_room_page.tap_TransitionRoom_hotkey()
            time.sleep(DELAY_TIME)

            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_4_2_1.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_4_2_1.png'
            current_preview = transition_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)

        with uuid("042df966-311e-4baa-8068-88e35767705d") as case:
            # 2.4.3.Only one image/video clip on timeline > Apply My Favorite Transition to All Videos
            main_page.close_and_restart_app()
            time.sleep(DELAY_TIME * 3)
            main_page.insert_media("Food.jpg")
            time.sleep(DELAY_TIME)
            transition_room_page.tap_TransitionRoom_hotkey()
            time.sleep(DELAY_TIME)
            transition_room_page.select_LibraryRoom_category('All Content')
            main_page.select_library_icon_view_media('Arrow 2')
            transition_room_page.select_RightClickMenu_Addto('My Favorites')
            time.sleep(DELAY_TIME)
            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)
            transition_room_page.select_right_click_menu('Apply My Favorite Transition to All Videos')

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_4_3_1.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_4_3_1.png'
            current_preview = transition_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)

            # Remove transition from My Favorites
            transition_room_page.select_LibraryRoom_category('My Favorites')
            main_page.select_library_icon_view_media('Arrow 2')
            transition_room_page.select_RightClickMenu_RemoveFromFavorites()

        with uuid("c1456c26-b288-4803-acb2-e7d739e8505d") as case:
            # 2.4.3.Only one image/video clip on timeline > Apply Fading Transition to All Videos

            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)
            transition_room_page.select_right_click_menu('Apply Fading Transition to All Videos')

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_4_3_2.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_4_3_2.png'
            current_preview = transition_room_page.snapshot(
                locator=L.library_preview.display_panel, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)

        with uuid("f5f0dfad-48af-4fc8-8ce8-16b72c3e158a") as case:
            # 2.4.4.Only one audio clip on timeline > Apply My Favorite Transition to All Videos
            main_page.close_and_restart_app()
            time.sleep(DELAY_TIME * 3)
            main_page.insert_media("Mahoroba.mp3")
            time.sleep(DELAY_TIME)
            transition_room_page.tap_TransitionRoom_hotkey()
            time.sleep(DELAY_TIME)
            transition_room_page.select_LibraryRoom_category('All Content')
            main_page.select_library_icon_view_media('Arrow 2')
            transition_room_page.select_RightClickMenu_Addto('My Favorites')
            time.sleep(DELAY_TIME)
            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_4_4_1.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_4_4_1.png'
            current_preview = transition_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)

            # Remove transition from My Favorites
            time.sleep(DELAY_TIME * 3)
            transition_room_page.select_LibraryRoom_category('My Favorites')
            main_page.select_library_icon_view_media('Arrow 2')
            transition_room_page.select_RightClickMenu_RemoveFromFavorites()

        with uuid("93cb5b3d-8f0e-4c18-a3a6-e50706b3aa8f") as case:
            # 2.4.4.Only one audio clip on timeline > Apply Fading Transition to All Videos

            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)

            image_full_path = Auto_Ground_Truth_Folder + 'transition_room_2_4_4_2.png'
            ground_truth = Ground_Truth_Folder + 'transition_room_2_4_4_2.png'
            current_preview = transition_room_page.snapshot(
                locator=L.media_room.library_listview.main_frame, file_name=image_full_path)
            check_result = transition_room_page.compare(ground_truth, current_preview)
            case.result = check_result

            transition_room_page.exist_click(L.media_room.library_menu.btn_menu)

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    90405a16-6e91-4991-b792-d34ed9671291
                    8e12afd1-42b3-4ebe-9b1b-a4eaa15db71b
                    29cd1be3-a1bd-4de2-bef9-63725a293c6c
                    d40f5082-efe6-4ab0-8790-f8b984692e61
                    4311bcf8-2f0b-49c6-b388-b5d8fd5aa4be
                    5eb663a0-e823-479c-88a0-fd53c8da8225
                    ca7b0f9d-a23b-437f-847c-812495dfaf67
                    92cf1ae1-081c-41cb-8b5c-b7491e98c932
                    7f0f1f35-e984-40b4-8fe9-86138d3ceab8
                    9c38ea25-c930-48ca-8344-8decc7f5548f
                    1131ab28-541f-4975-a637-50542fc160ed
                    5e1bfa2b-523a-4936-a097-10b2b3814d43
                    d7a7ebe2-4d5c-4fbc-94bb-cf34378c5171
                    db615ab4-6a4e-4892-834a-2b8a79bcfbb4
                    008775eb-0fbf-441b-a4c1-d33384abebc2
                    e20da256-f80e-43af-85b4-0de429a81c97
                    60d98d71-6973-4a9d-b036-735ab738ec2c
                    c04bd3fb-3e93-4ea2-bbe0-1f3a6c1730e0
                    fed1f99e-e373-47f7-9c96-5e70045ed851
                    97c21ab8-1069-4610-9f61-18701c8f5f92
                    bc2d7462-412b-487e-ac37-97481a645dfd
                    a390098e-6d3c-48a8-9d24-6a2cdec6f69c
                    7ef0cc89-29c1-437d-919c-2f9d2e8cba74
                    a96e7e7f-71cb-4304-ba30-9fc4d9ac3abc
                    46799983-e11b-4999-a0b8-83a3d9f68bfa
                    90362ea6-874c-42f7-87c9-06eb9b73fcfb
                    825b710b-4208-4185-aa0b-08beac0c6a57
                    c2c9c8e6-0d23-4d38-b9ec-f8e759d483ea
                    88f27d91-3f34-4637-a58e-efc162d3b5d4
                    982aeb0e-d452-4115-98e1-7256ac3561f7
                    b06a1c46-bddd-468c-9c12-0148c60eb900
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'