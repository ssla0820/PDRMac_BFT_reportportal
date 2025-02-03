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
media_room_page = PageFactory().get_page_object('media_room_page', mwc)
timeline_operation_page = PageFactory().get_page_object('timeline_operation_page', mwc)
tips_area_page = PageFactory().get_page_object('tips_area_page', mwc)
project_new_page = PageFactory().get_page_object('project_new_page', mwc)
effect_room_page = PageFactory().get_page_object('effect_room_page', mwc)
transition_room_page = PageFactory().get_page_object('transition_room_page', mwc)
pip_room_page = PageFactory().get_page_object('pip_room_page', mwc)
title_room_page = PageFactory().get_page_object('title_room_page', mwc)
playback_window_page = PageFactory().get_page_object('playback_window_page', mwc)
particle_room_page = PageFactory().get_page_object('particle_room_page', mwc)
# create driver & page <<

# For Report >>
report = MyReport("MyReport", driver=mwc, html_name="Project (New Open Save Pack).html")
uuid = report.uuid
exception_screenshot = report.exception_screenshot
report.ovInfo.update(build_info)
# For Report <<

# For Ground Truth / Test Material folder
Ground_Truth_Folder = app.ground_truth_root + '/Project_New_Open_Save_Pack/'
Auto_Ground_Truth_Folder = app.auto_ground_truth_root + '/Project_New_Open_Save_Pack/'
Test_Material_Folder = app.testing_material

DELAY_TIME = 1


class Test_Project_New_Open_Save_Pack():
    @pytest.fixture(autouse=True)
    def initial(self):
        """
        for common setup & teardown
        if having session/module scope, would run 'session/module' scope before autouse
        """
        main_page.start_app()
        media_room_page.find(L.media_room.library_listview.unit_collection_view_item, timeout=10)
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
            google_sheet_execution_log_init('Project_New_Open_Save_Pack')

    @classmethod
    def teardown_class(cls):
        logger('teardown_class - export report')
        report.export()
        logger(
            f"project new open save pack result={report.get_ovinfo('pass')}, {report.fail_number=}, {report.get_ovinfo('na')}, {report.get_ovinfo('skip')}, {report.get_ovinfo('duration')}")
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
        with uuid('e3c16e26-ee1f-4126-8e9b-878636a22031') as case:
            # 1. General
            # 1.1. New Project
            # 1.1.1.  Click via [File] menu w/o edited
            # 1. New a PDR project (*.pds) as settings directly if the project is not edited
            check_result_1 = main_page.top_menu_bar_file_new_project()
            media_room_page.find(L.media_room.library_listview.unit_collection_view_item, timeout=10)
            default_project_name = main_page.get_project_name()
            check_result_2 = False if not default_project_name == 'New Untitled Project' else True
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_1_1_1-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_1_1_1-1.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.library, file_name=image_full_path)
            check_result_3 = main_page.compare(ground_truth, current_preview)
            case.result = check_result_1 and check_result_2 and check_result_3

        with uuid('e445d49e-31dd-4613-a091-78d2f746bb60') as case:
            # 1.1. New Project
            # 1.1.2. [Command] + [N] display w/o edited
            # 1. New a PDR project (*.pds) as settings directly if the project is not edited
            main_page.tap_CreateNewProject_hotkey()
            media_room_page.find(L.media_room.library_listview.unit_collection_view_item, timeout=10)
            default_project_name = main_page.get_project_name()
            check_result_1 = False if not default_project_name == 'New Untitled Project' else True
            time.sleep(DELAY_TIME * 3)
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_1_1_2-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_1_1_2-1.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.library, file_name=image_full_path)
            check_result_2 = main_page.compare(ground_truth, current_preview)
            case.result = check_result_1 and check_result_2

        with uuid('fdddc3dc-84cf-4045-918f-1c75577deaae') as case:
            # 1.1. New Project
            # 1.1.3. When the project was edited
            # Prompt "Save project" dialogue before new a project
            main_page.insert_media('Food.jpg')
            time.sleep(DELAY_TIME * 2)
            main_page.tap_CreateNewProject_hotkey()
            save_project_confirm_dialog = project_new_page.is_exist(L.base.confirm_dialog.main_window, timeout=5)
            check_result = False if not save_project_confirm_dialog else True
            case.result = check_result

            project_new_page.click(L.base.confirm_dialog.btn_no)

        with uuid('fb46a477-3001-4849-b137-a644e0faa59e') as case:
            # 1.2. New Workspace
            # 1.2.1. via [Shift] + [Command] + [W] hotkey
            # Clear timeline directly if the project is not edited yet
            project_new_page.tap_menu_bar_file_open_project()
            project_new_page.open_project.select_project(
                'project_operation_1.pds', Test_Material_Folder + 'project_operation/')
            project_new_page.exist_click(L.main.open_file_dialog.btn_open)
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')

            main_page.tap_NewWorkspace_hotkey()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_1_2_1-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_1_2_1-1.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('f8e3ddb9-aa75-4813-bb10-c1b947e6f3a2') as case:
            # 1.2. New Workspace
            # 1.2.2. When the project was edited
            # 1. Prompt "Save project" dialogue before new a project
            main_page.insert_media('Landscape 01.jpg')
            time.sleep(DELAY_TIME * 2)
            main_page.tap_NewWorkspace_hotkey()
            save_project_confirm_dialog = project_new_page.is_exist(L.base.confirm_dialog.main_window, timeout=5)
            check_result = False if not save_project_confirm_dialog else True
            case.result = check_result

            project_new_page.click(L.base.quit_dialog.cancel)

        with uuid('e5bcb34d-554b-42c0-b9b0-91bd9148dadc') as case:
            # 1.2. New Workspace
            # 1.2.2. When the project was edited
            # 2. New workspace after saving project
            check_result_1 = project_new_page.save_project(
                'project_operation_2', Test_Material_Folder + 'project_operation/')

            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_1_2_2-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_1_2_2-1.png'
            current_preview = main_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result_2 = main_page.compare(ground_truth, current_preview)
            case.result = check_result_1 and check_result_2

        with uuid('3a652f64-239e-41e3-820a-34489bf00555') as case:
            # 1.5. Save Project
            # 1.5.2. via [Command] + [S] hotkey
            # Save PDR project (*.pds) correctly as settings
            case.result = check_result_1

        with uuid('5cafcafb-f2b6-4f64-b47d-f00a8b05e77c') as case:
            # 1.3. Open Project
            # 1.3.1. Before editing project > Click via [File] menu -> (Open Project..) w/o edited
            # Open saved PDR project (*.pds) correctly as previous settings if current project has not been edited yet
            project_new_page.tap_menu_bar_file_open_project()
            time.sleep(DELAY_TIME*1.5)
            project_new_page.open_project.select_project(
                'project_operation_1.pds', Test_Material_Folder + 'project_operation/')
            project_new_page.exist_click(L.main.open_file_dialog.btn_open)
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')

            current_project_name = project_new_page.exist(L.main.top_project_name).AXValue
            check_result = False if not current_project_name == 'project_operation_1' else True
            case.result = check_result

        with uuid('b9c193bb-8721-4e36-a3df-954ccd036d2e') as case:
            # 1.3. Open Project
            # 1.3.1. Before editing project > via [Command] + [O] hotkey
            # Open saved PDR project (*.pds) correctly as previous settings if current project has not been edited yet
            project_new_page.tap_OpenProject_hotkey()
            time.sleep(DELAY_TIME * 1.5)
            project_new_page.open_project.select_project(
                'project_operation_2.pds', Test_Material_Folder + 'project_operation/')
            project_new_page.exist_click(L.main.open_file_dialog.btn_open)
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')

            current_project_name = project_new_page.exist(L.main.top_project_name).AXValue
            check_result = False if not current_project_name == 'project_operation_2' else True
            case.result = check_result

        with uuid('c00b7af9-7c3c-4f68-bc7b-dd323251cf6c') as case:
            # 1.3. Open Project
            # 1.3.2. After editing project > via [Command] + [O] hotkey --> Click [No]
            # Prompt "Save project" dialogue before opening project and
            # Select [No] to discard changes and open project directly
            main_page.select_timeline_media('Landscape 01.jpg')
            timeline_operation_page.press_del_key()
            project_new_page.tap_OpenProject_hotkey()
            project_new_page.click(L.base.confirm_dialog.btn_no)
            time.sleep(DELAY_TIME * 1.5)
            project_new_page.open_project.select_project(
                'project_operation_1.pds', Test_Material_Folder + 'project_operation/')
            project_new_page.exist_click(L.main.open_file_dialog.btn_open)
            main_page.handle_merge_media_to_current_library_dialog(option='no', do_not_show_again='no')

            current_project_name = project_new_page.exist(L.main.top_project_name).AXValue
            check_result = False if not current_project_name == 'project_operation_1' else True
            case.result = check_result

        with uuid('c917cb67-49d8-45a7-8285-0c1b5be6d783') as case:
            # 1.3. Open Project
            # 1.3.3. Open PDR Project
            # Able to open .pds correctly
            case.result = check_result

        with uuid('f4247acf-b350-4f9c-87dc-5240f3e733b2') as case:
            # 1.7. Pack Project Material
            # 1.7.1. via [File] menu
            # Pack whole test materials and save as PDR project (*.pds) correctly as previous settings
            main_page.top_menu_bar_file_new_project()
            main_page.insert_media('Skateboard 01.mp4')
            check_result_1 = project_new_page.menu_bar_file_pack_project_materials(
                'project_operation_3', Test_Material_Folder + 'project_operation/')

            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == 'New Untitled Project*' else True
            case.result = check_result_1 and check_result_2

        with uuid('796ca11f-f0f2-4d22-83ee-64e237759f0d') as case:
            # 1.3. Open Project
            # 1.3.4. PDR Pack Project
            # Able to open packed project correctly
            check_result_1 = project_new_page.open_pdk_project(
                Test_Material_Folder + 'project_operation/project_operation_3.pdk',
                Test_Material_Folder + 'project_operation/pdk_uncompress')
            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == 'project_operation_3' else True
            case.result = check_result_1 and check_result_2

        with uuid('b20a04d7-6f5e-4609-a9dd-1560b0806cae') as case:
            # 1.4. Open Recent Project
            # 1.4.1. via [File] menu
            # Able to find recent projects in the menu
            main_page.top_menu_bar_file_open_recent_projects()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_1_4_1-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_1_4_1-1.png'
            current_preview = main_page.snapshot(
                locator=L.base.main_window, file_name=image_full_path)
            check_result = main_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.press_esc_key()

        with uuid('b40baa75-04c8-4d0e-8777-da11bf395e1e') as case:
            # 1.6. Save As...
            # 1.6.1. via [File] menu
            # Save PDR project (*.pds) correctly as settings
            check_result_1 = main_page.top_menu_bar_file_save_project_as()
            project_new_page.save_file.handle_save_file(
                'project_operation_4', Test_Material_Folder + 'project_operation/')

            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == 'project_operation_4' else True
            case.result = check_result_1 and check_result_2

        with uuid('3511ad99-d147-461a-a094-37941470639c') as case:
            # 1.6. Save As...
            # 1.6.2. via [Shift] + [Command] + [S] hotkey
            # Save PDR project (*.pds) correctly as settings
            project_new_page.tap_SaveProjectAs_hotkey()
            project_new_page.save_file.handle_save_file(
                'project_operation_5', Test_Material_Folder + 'project_operation/')

            current_project_name = main_page.get_project_name()
            check_result = False if not current_project_name == 'project_operation_5' else True
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_2(self):
        main_page.set_project_aspect_ratio('4_3')

        # all video/photo/audio to timeline
        main_page.insert_media('Skateboard 01.mp4', aspect_ratio_conflict_option='no')
        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Food.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Landscape 01.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Speaking Out.mp3')
        tips_area_page.click_TipsArea_btn_insert_audio(option=1)

        main_page.enter_room(3)  # Enter Effect room, add an effect to timeline
        effect_room_page.apply_effect_to_video('Black and White', track_index=0, clip_index=3)
        timeline_operation_page.deselect_clip(track_index=0, last_clip_index=3, movement=100)
        playback_window_page.Edit_Timeline_PreviewOperation('Stop')

        main_page.timeline_select_track(track_no=2)  # add a particle effect to track_2
        main_page.enter_room(5)  # Enter Particle room
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Maple')
        tips_area_page.click_TipsArea_btn_insert()

        main_page.enter_room(1)  # Enter Title room, add a title to track_2
        main_page.select_library_icon_view_media('Default')
        tips_area_page.click_TipsArea_btn_insert(option=1)

        main_page.enter_room(4)  # Enter PiP room, add a pip to track_2
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Dialog_03')
        tips_area_page.click_TipsArea_btn_insert(option=1)  # insert

        main_page.enter_room(2)  # Enter Transition room, apply transition to all media
        transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Cross')

        with uuid('f48393f5-e0a7-4ab0-8722-dd4c864a3a80') as case:
            # 1.5. Save Project
            # 1.5.1. via [File] menu
            # Save PDR project (*.pds) correctly as settings
            check_result = project_new_page.tap_menu_bar_file_save_project()
            case.result = check_result

        with uuid('0e2c9911-5771-4fcc-8307-810b67c4c8bd') as case:
            # 2.3. Name
            # 2.3.1. Type > Untitled (Default)
            # Save project w/ name correctly
            if not project_new_page.is_exist(L.main.save_file_dialog.main_window):
                check_result = False
            else:
                default_file_name = project_new_page.find(L.main.save_file_dialog.input_save_as).AXValue
                check_result = False if not default_file_name == 'Untitled' else True
            case.result = check_result

        with uuid('f51a3635-954c-4cb5-807d-d2747e177274') as case:
            # 2.4. Tags
            # 2.4.1. Type > Untitled (Default)
            # Save project w/ tags correctly
            check_result = project_new_page.save_file.check_default_tags()
            case.result = check_result

        with uuid('ee6de977-4d34-41a3-aca4-71b1f8f3ff91') as case:
            # 2.7. Path
            # 2.7.1. Type > (Default)
            # Save PDR project w/ selected path correctly
            img_before = main_page.screenshot()
            time.sleep(DELAY_TIME)
            project_new_page.save_file.unfold_window()
            time.sleep(DELAY_TIME)
            project_new_page.save_file.set_path(Test_Material_Folder + 'project_operation/')

            check_result = main_page.wait_for_image_changes(img_before)
            case.result = check_result

        with uuid('737b605d-e38f-43ab-8bdf-a7bff22d9c6a') as case:
            # 2.5. [<] & [>] buttons
            # Enter previous & next folder correctly
            check_result_1 = project_new_page.save_file.click_previous_folder()
            time.sleep(DELAY_TIME)
            img_before = main_page.snapshot(L.base.file_picker.main)
            time.sleep(DELAY_TIME)
            check_result_3 = project_new_page.save_file.click_next_folder()
            main_page.wait_for_image_changes(img_before, locator=L.base.file_picker.main, similarity=0.99)

            case.result = check_result_1 and check_result_3

        with uuid('861a94f9-840e-482d-8412-803e167b56b1') as case:
            # 2.6. Display Controls
            # 2.6.1. Show Sidebar > On & Off
            # Show & hide sidebar correctly
            check_result_1 = project_new_page.save_file.click_grouping_show_sidebar(is_enable=False)
            time.sleep(DELAY_TIME)
            img_before = main_page.snapshot(L.base.file_picker.main)
            check_result_3 = project_new_page.save_file.click_grouping_show_sidebar(is_enable=True)
            main_page.wait_for_image_changes(img_before, locator=L.base.file_picker.main, similarity=0.99)

            case.result = check_result_1 and check_result_3

        with uuid('320c7bb9-9903-4447-b5d4-e10f88e7e701') as case:
            # 2.6. Display Controls
            # 2.6.2. Show items as > Icons
            # Switch item display correctly
            img_before = main_page.snapshot(L.base.file_picker.main)
            time.sleep(DELAY_TIME)
            check_result_1 = project_new_page.save_file.click_grouping_show_item_as_icons()
            main_page.wait_for_image_changes(img_before, locator=L.base.file_picker.main, similarity=0.99)
            case.result = check_result_1

        with uuid('ab403d3b-cb3f-49ff-94cc-77aa261cb761') as case:
            # 2.6. Display Controls
            # 2.6.2. Show items as > List
            # Show item as settings correctly
            img_before = main_page.snapshot(L.base.file_picker.main)
            time.sleep(DELAY_TIME)
            check_result_1 = project_new_page.save_file.click_grouping_show_item_as_list()
            main_page.wait_for_image_changes(img_before, locator=L.base.file_picker.main, similarity=0.99)
            case.result = check_result_1

        with uuid('71057479-b8a7-43ca-bb91-e3524bce58b3') as case:
            # 2.6. Display Controls
            # 2.6.2. Show items as > Columns
            # Show item as settings correctly
            img_before = main_page.snapshot(L.base.file_picker.main)
            time.sleep(DELAY_TIME)
            check_result_1 = project_new_page.save_file.click_grouping_show_item_as_columns()
            main_page.wait_for_image_changes(img_before, locator=L.base.file_picker.main, similarity=0.99)
            case.result = check_result_1

        with uuid('ab001ddf-282c-40b1-87c7-0f560c77554f') as case:
            # 2. Save (As) Project
            # 2.1. Library
            # 2.1.1. Media (Photo, Video, Audio)
            # Save project w/ Content correctly
            check_result_1 = project_new_page.save_file.click_save()
            time.sleep(DELAY_TIME * 5)

            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == 'Untitled' else True
            case.result = check_result_1 and check_result_2

        with uuid('27e7300f-e18b-4c62-a0ae-86e0e14c1a39') as case:
            # 2.1. Library
            # 2.1.2. Effect
            # Save project w/ Content correctly
            case.result = check_result_1 and check_result_2

        with uuid('13d69fe2-9ac0-4a29-af7f-8bfe5297d7a3') as case:
            # 2.1. Library
            # 2.1.3. PiP
            # Save project w/ Content correctly
            case.result = check_result_1 and check_result_2

        with uuid('34d07843-bf33-45c6-9673-f0a15035a6e4') as case:
            # 2.1. Library
            # 2.1.4. Particle
            # Save project w/ Content correctly
            case.result = check_result_1 and check_result_2

        with uuid('ac05f5ec-169f-4181-b0cc-26cc40115452') as case:
            # 2.1. Library
            # 2.1.5. Title
            # Save project w/ Content correctly
            case.result = check_result_1 and check_result_2

        with uuid('e3217884-0fc5-4261-a51e-94c31993b395') as case:
            # 2.1. Library
            # 2.1.6. Transition
            # Save project w/ Content correctly
            case.result = check_result_1 and check_result_2

        with uuid('7453cfc3-48dc-424a-9171-53727d680f57') as case:
            # 2.2. Aspect Ratio
            # 2.2.1. 4:3
            # Save project w/ Content correctly
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_3(self):
        main_page.set_project_aspect_ratio('9_16')

        # all video/photo/audio to timeline
        main_page.insert_media('Skateboard 01.mp4', aspect_ratio_conflict_option='no')
        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Food.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Landscape 01.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Speaking Out.mp3')
        tips_area_page.click_TipsArea_btn_insert_audio(option=1)

        main_page.enter_room(3)  # Enter Effect room, add an effect to timeline
        time.sleep(2)
        effect_room_page.apply_effect_to_video('Black and White', track_index=0, clip_index=3)
        timeline_operation_page.deselect_clip(track_index=0, last_clip_index=3, movement=100)
        playback_window_page.Edit_Timeline_PreviewOperation('Stop')

        main_page.timeline_select_track(track_no=2)  # add a particle effect to track_2
        main_page.enter_room(5)  # Enter Particle room
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Maple')
        tips_area_page.click_TipsArea_btn_insert()

        main_page.enter_room(1)  # Enter Title room, add a title to track_2
        main_page.select_library_icon_view_media('Default')
        tips_area_page.click_TipsArea_btn_insert(option=1)

        main_page.enter_room(4)  # Enter PiP room, add a pip to track_2
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Dialog_03')
        tips_area_page.click_TipsArea_btn_insert(option=1)  # insert

        main_page.enter_room(2)  # Enter Transition room, apply transition to all media
        transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Cross')

        project_new_page.tap_menu_bar_file_save_project()

        with uuid('6f05c14f-12ed-4d61-9277-3981bacc3c22') as case:
            # 2.3. Name
            # 2.3.1. Type > Unicode
            # Save project w/ name correctly
            if not project_new_page.is_exist(L.main.save_file_dialog.main_window):
                check_result = False
            else:
                check_result = project_new_page.save_file.set_project_name('9_16_許功蓋_℃ꮤ®¶ÅËæ¾')
            case.result = check_result

        with uuid('df7496b7-a0ad-453c-91b6-8e008eff380c') as case:
            # 2.3. Name
            # 2.3.1. Type > Big 5 (許功蓋)
            # Save project w/ name correctly
            case.result = check_result

        with uuid('5287686d-b2de-4b0b-ad61-bbd996ace11a') as case:
            # 2.4. Tags
            # 2.4.1. Type > Unicode
            # Save project w/ tags correctly
            check_result_1 = project_new_page.save_file.set_tags_by_input_string('℃ꮤ®¶ÅËæ¾')
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_2_4_1-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_2_4_1-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)
            case.result = check_result_1 and check_result_2

        with uuid('df3abcfe-9598-495d-859b-e20effd00ac8') as case:
            # 2.4. Tags
            # 2.4.1. Type > Big 5 (許功蓋)
            # Save project w/ tags correctly
            check_result_1 = project_new_page.save_file.set_tags_by_input_string('許功蓋')
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_2_4_1-2.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_2_4_1-2.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)
            case.result = check_result_1 and check_result_2

        with uuid('ccd02236-c3f7-41fc-95f5-f3e21220b62c') as case:
            # 2.7. Path
            # 2.7.1. Type > Unicode
            # Save PDR project w/ selected path correctly
            project_new_page.save_file.unfold_window()
            time.sleep(DELAY_TIME)
            project_new_page.save_file.set_path(Test_Material_Folder + 'project_operation/路徑許功蓋_℃ꮤ®¶ÅËæ¾/')

            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_2_7_1-2.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_2_7_1-2.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result = project_new_page.compare(ground_truth, current_preview, similarity=0.7)
            case.result = check_result

        with uuid('09a30ec6-d504-4dc4-959b-e94df550a67f') as case:
            # 2.7. Path
            # 2.7.1. Type > Big 5 (許功蓋)
            # Save PDR project w/ selected path correctly
            case.result = check_result

        with uuid('5df90234-5bf8-4ff6-9bd5-1d19ac3a4f8a') as case:
            # 2.2. Aspect Ratio
            # 2.2.3. 9:16
            # Save project w/ Content correctly
            check_result_1 = project_new_page.save_file.click_save()
            time.sleep(DELAY_TIME * 5)

            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == '9_16_許功蓋_℃ꮤ®¶ÅËæ¾' else True
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_4(self):
        main_page.set_project_aspect_ratio('1_1')

        # all video/photo/audio to timeline
        main_page.insert_media('Skateboard 01.mp4', aspect_ratio_conflict_option='no')
        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Food.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Landscape 01.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Speaking Out.mp3')
        tips_area_page.click_TipsArea_btn_insert_audio(option=1)

        main_page.enter_room(3)  # Enter Effect room, add an effect to timeline
        effect_room_page.apply_effect_to_video('Black and White', track_index=0, clip_index=3)
        timeline_operation_page.deselect_clip(track_index=0, last_clip_index=3, movement=100)
        playback_window_page.Edit_Timeline_PreviewOperation('Stop')

        main_page.timeline_select_track(track_no=2)  # add a particle effect to track_2
        main_page.enter_room(5)  # Enter Particle room
        time.sleep(2)
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Maple')
        tips_area_page.click_TipsArea_btn_insert()

        main_page.enter_room(1)  # Enter Title room, add a title to track_2
        main_page.select_library_icon_view_media('Default')
        tips_area_page.click_TipsArea_btn_insert(option=1)

        main_page.enter_room(4)  # Enter PiP room, add a pip to track_2
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Dialog_03')
        tips_area_page.click_TipsArea_btn_insert(option=1)  # insert

        main_page.enter_room(2)  # Enter Transition room, apply transition to all media
        transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Cross')

        project_new_page.tap_menu_bar_file_save_project()

        with uuid('d738d6db-4e6a-4490-97a7-cfffa5fe8d40') as case:
            # 2.3. Name
            # 2.3.1. Type > Symbol
            # Save project w/ name correctly
            if not project_new_page.is_exist(L.main.save_file_dialog.main_window):
                check_result = False
            else:
                check_result = project_new_page.save_file.set_project_name('1_1_@#$%^&* ()_+-{} |[];? <>!')
            case.result = check_result

        with uuid('de6b339a-64dc-4fbb-856f-81e4ad52a832') as case:
            # 2.3. Name
            # 2.3.1. Type > Space Character included
            # Save project w/ name correctly
            case.result = check_result

        with uuid('ac6adbf8-3a6c-493e-b542-75f322d3fa69') as case:
            # 2.4. Tags
            # 2.4.1. Type > Symbol
            # Save project w/ tags correctly
            check_result_1 = project_new_page.save_file.set_tags_by_input_string('@#$%^&*()')
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_2_4_1-3.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_2_4_1-3.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.80)
            case.result = check_result_1 and check_result_2

        with uuid('5b8c6b2d-f945-49a7-8647-1756eec24abb') as case:
            # 2.4. Tags
            # 2.4.1. Type > Space Character included
            # Save project w/ tags correctly
            check_result_1 = project_new_page.save_file.set_tags_by_input_string('T  T')
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_2_4_1-4.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_2_4_1-4.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.80)
            case.result = check_result_1 and check_result_2

        with uuid('69b27f94-725c-4403-8d88-ed01222e9a2a') as case:
            # 2.4. Tags
            # 2.4.1. Type > Space Character Only
            # Save project w/ tags correctly
            check_result_1 = project_new_page.save_file.set_tags_by_input_string('  ')
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_2_4_1-5.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_2_4_1-5.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.80)
            case.result = check_result_1 and check_result_2

        with uuid('d3d15d80-1bf7-4496-b9fd-0ec63ac40aa8') as case:
            # 2.7. Path
            # 2.7.1. Type > Symbol
            # Save PDR project w/ selected path correctly
            project_new_page.save_file.unfold_window()
            time.sleep(DELAY_TIME)
            project_new_page.save_file.set_path(Test_Material_Folder + 'project_operation/@#$%^&*()_+{}[]/')

            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_2_7_1-3.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_2_7_1-3.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result = project_new_page.compare(ground_truth, current_preview, similarity=0.7)
            case.result = check_result

        with uuid('133ae599-4dd9-4d7c-ab8e-ea20f7d633b1') as case:
            # 2.2. Aspect Ratio
            # 2.2.4. 1:1
            # Save project w/ Content correctly
            check_result_1 = project_new_page.save_file.click_save()
            time.sleep(DELAY_TIME * 5)

            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == '1_1_@#$%^&* ()_+-{} |[];? <>!' else True
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_5(self):
        main_page.set_project_aspect_ratio('16_9')

        # all video/photo/audio to timeline
        main_page.insert_media('Skateboard 01.mp4', aspect_ratio_conflict_option='no')
        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Food.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Landscape 01.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Speaking Out.mp3')
        tips_area_page.click_TipsArea_btn_insert_audio(option=1)

        main_page.enter_room(3)  # Enter Effect room, add an effect to timeline
        effect_room_page.apply_effect_to_video('Black and White', track_index=0, clip_index=3)
        timeline_operation_page.deselect_clip(track_index=0, last_clip_index=3, movement=100)
        playback_window_page.Edit_Timeline_PreviewOperation('Stop')

        main_page.timeline_select_track(track_no=2)  # add a particle effect to track_2
        main_page.enter_room(5)  # Enter Particle room
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Maple')
        tips_area_page.click_TipsArea_btn_insert()

        main_page.enter_room(1)  # Enter Title room, add a title to track_2
        main_page.select_library_icon_view_media('Default')
        tips_area_page.click_TipsArea_btn_insert(option=1)

        main_page.enter_room(4)  # Enter PiP room, add a pip to track_2
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Dialog_03')
        tips_area_page.click_TipsArea_btn_insert(option=1)  # insert

        main_page.enter_room(2)  # Enter Transition room, apply transition to all media
        transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Cross')

        project_new_page.tap_menu_bar_file_save_project()

        with uuid('e6735fe6-4c26-4e2c-b0d0-cd61c3f1c587') as case:
            # 2.3. Name
            # 2.3.1. Type > Longest
            # Save project w/ name correctly
            if not project_new_page.is_exist(L.main.save_file_dialog.main_window):
                check_result = False
            else:
                check_result = project_new_page.save_file.set_project_name(
                    '16_9_12345678901234567890123456789012345678901234567890123456789012345678901234567890'
                       + '12345678901234567890123456789012345678901234567890123456789012345678901234567890'
                       + '12345678901234567890123456789012345678901234567890123456789012345678901234567890'
                       + '123456')
            case.result = check_result

        with uuid('d3d958f5-4ff4-49dd-b97a-d95e086439e0') as case:
            # 2.4. Tags
            # 2.4.1. Type > Yellow
            # Save project w/ tags correctly
            check_result_1 = project_new_page.save_file.set_tag_to_yellow()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_2_4_1-6.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_2_4_1-6.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.80)
            case.result = check_result_1 and check_result_2

        with uuid('b5736b58-fa50-4897-8b74-c20cae133e36') as case:
            # 2.4. Tags
            # 2.4.1. Type > Work
            # Save project w/ tags correctly
            check_result_1 = project_new_page.save_file.set_tag_to_work()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_2_4_1-7.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_2_4_1-7.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.80)
            case.result = check_result_1 and check_result_2

        with uuid('1ebda4e3-5943-4d65-a95d-e7f04d7dff8e') as case:
            # 2.4. Tags
            # 2.4.2. Show All
            # show all tag list correctly
            check_result_1 = project_new_page.save_file.click_tags_show_all()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_2_4_2-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_2_4_2-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.80)
            case.result = check_result_1 and check_result_2

        with uuid('942502b9-86cc-4a20-8102-40e88b753678') as case:
            # 2.9. Save
            # Save PDR project (*.pds) correctly as settings
            project_new_page.save_file.unfold_window()
            time.sleep(DELAY_TIME)
            project_new_page.save_file.set_path(Test_Material_Folder + 'project_operation/')

            check_result_1 = project_new_page.save_file.click_save()
            time.sleep(DELAY_TIME * 5)

            current_project_name = main_page.get_project_name()
            check_result_2 = False if not \
                current_project_name == '16_9_123456789012345678901234567890123456789012345678901234567890' \
                                        '1234567890123456789012345678901234567890123456789012345678901234567890' \
                                        '1234567890123456789012345678901234567890123456789012345678901234567890' \
                                        '1234567890123456789012345678901234567890123456' else True
            case.result = check_result_1 and check_result_2

        with uuid('4c4a9cf8-d913-4cda-a02c-0cfca4991dba') as case:
            # 2.2. Aspect Ratio
            # 2.2.2. 16:9
            # Save project w/ Content correctly
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_1_1_6(self):
        project_new_page.tap_menu_bar_file_save_project()

        with uuid('7ec2900a-0e10-4436-975d-3e5f8f83c7a6') as case:
            # 2.3. Name
            # 2.3.1. Type > * Empty
            # grey out [Save] button
            project_new_page.save_file.clear_save_as()
            time.sleep(DELAY_TIME)

            btn_status = project_new_page.exist(L.base.file_picker.btn_save).AXEnabled
            check_result = True if not btn_status else False
            case.result = check_result

        with uuid('3d116334-cfe2-46de-a093-d6271b985411') as case:
            # 2.3. Name
            # 2.3.1. Type > Space Character Only
            # Save project w/ name correctly
            check_result = project_new_page.save_file.set_project_name('    ')
            case.result = check_result

        with uuid('4394ddf5-4f56-45e0-9f45-cb5f65a90c63') as case:
            # 2.8. New Folder
            # 2.8.1. Method > via [New Folder] icon
            # Enter New Folder dialog correctly
            '''
            project_new_page.save_file.unfold_window()
            time.sleep(DELAY_TIME)
            logger(Test_Material_Folder + 'project_operation/')
            project_new_page.save_file.set_path(Test_Material_Folder + 'project_operation/')
            time.sleep(DELAY_TIME)
            project_new_page.save_file.click_top_new_folder()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_2_8_1-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_2_8_1-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.new_folder.main, file_name=image_full_path)
            check_result = project_new_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.press_esc_key()

            '''
            case.result = None
            case.fail_log = 'MacOS limitation'

        with uuid('ca20935a-fa50-4069-9ee0-ae40903d3087') as case:
            # 2.8. New Folder
            # 2.8.1. Method > via [New Folder] button
            # Enter New Folder dialog correctly
            project_new_page.save_file.unfold_window()
            time.sleep(DELAY_TIME)
            project_new_page.save_file.set_path(Test_Material_Folder + 'project_operation/')
            time.sleep(DELAY_TIME)
            project_new_page.save_file.click_bottom_new_folder()
            time.sleep(DELAY_TIME*3)

            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_2_8_1-2.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_2_8_1-2.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.new_folder.main, file_name=image_full_path)
            check_result = project_new_page.compare(ground_truth, current_preview)
            case.result = check_result

        with uuid('83a5d4c4-de41-4259-b126-8e16fc7bbc6b') as case:
            # 2.8. New Folder
            # 2.8.2. Type > Untitled folder (Default)
            # Create new folder correctly as settings
            check_result = project_new_page.save_file.new_folder.check_default_folder_name()
            case.result = check_result

        with uuid('6ac1364e-f23d-4f01-8ee4-a3ddd64853ec') as case:
            # 2.8. New Folder
            # 2.8.2. Type > Unicode
            # Create new folder correctly as settings
            test_folder_path = Test_Material_Folder + 'project_operation/許功蓋_℃ꮤ®¶ÅËæ¾_@#$%^&*/'
            if os.path.exists(test_folder_path):
                import shutil
                shutil.rmtree(test_folder_path)

            check_result = project_new_page.save_file.new_folder.set_name('許功蓋_℃ꮤ®¶ÅËæ¾_@#$%^&*')
            case.result = check_result

        with uuid('e9ee8e66-8142-471c-a364-144ba2ea8fff') as case:
            # 2.8. New Folder
            # 2.8.2. Type > Big 5 (許功蓋)
            # Create new folder correctly as settings
            case.result = check_result

        with uuid('1df0af3c-e919-476e-a5ea-67dd945f15a2') as case:
            # 2.8. New Folder
            # 2.8.2. Type > Symbol
            # Create new folder correctly as settings
            case.result = check_result

        with uuid('37e96601-5c57-4ebe-9954-476939ecc19d') as case:
            # 2.8. New Folder
            # 2.8.4. Cancel > via [Cancel] button
            # Close dialog correctly
            project_new_page.save_file.new_folder.click_cancel()

            check_result_2 = project_new_page.is_not_exist(L.base.file_picker.new_folder.main)
            case.result = check_result_2

        with uuid('9ab673a2-5fad-4a83-b815-e9a6906bb8b6') as case:
            # 2.8. New Folder
            # 2.8.4. Cancel > via [ESC] key
            # Close dialog correctly
            project_new_page.save_file.click_bottom_new_folder()
            project_new_page.save_file.new_folder.set_name('許功蓋_℃ꮤ®¶ÅËæ¾_@#$%^&*')
            main_page.press_esc_key()

            check_result = project_new_page.is_not_exist(L.base.file_picker.new_folder.main)
            case.result = check_result

        with uuid('749bac6c-6ae7-49a8-8e82-4bfd61a48ec5') as case:
            # 2.8. New Folder
            # 2.8.3. Create > Create
            # Create new folder correctly
            project_new_page.save_file.click_bottom_new_folder()
            project_new_page.save_file.new_folder.set_name('許功蓋_℃ꮤ®¶ÅËæ¾_@#$%^&*')
            check_result_1 = project_new_page.save_file.new_folder.click_create()
            time.sleep(DELAY_TIME*1.5)

            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_2_8_3-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_2_8_3-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.80)
            case.result = check_result_1 and check_result_2

        with uuid('721c799b-2bed-408f-b91a-328f3d447cd7') as case:
            # 2.10. Cancel
            # 2.10.1. [Cancel] button
            # Close dialog correctly
            project_new_page.save_file.click_cancel()
            check_result_2 = project_new_page.is_not_exist(L.base.file_picker.main)
            case.result = check_result_2

        with uuid('4d2fa821-4551-474a-bf10-69789daa7d01') as case:
            # 2.10. Cancel
            # 2.10.2. [ESC] key
            # Close dialog correctly
            project_new_page.tap_menu_bar_file_save_project()
            time.sleep(DELAY_TIME * 2)
            main_page.press_esc_key()

            check_result = project_new_page.is_not_exist(L.base.file_picker.main)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_1(self):
        main_page.set_project_aspect_ratio('4_3')

        # all video/photo/audio to timeline
        main_page.insert_media('Skateboard 01.mp4', aspect_ratio_conflict_option='no')
        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Food.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Landscape 01.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Speaking Out.mp3')
        tips_area_page.click_TipsArea_btn_insert_audio(option=1)

        main_page.enter_room(3)  # Enter Effect room, add an effect to timeline
        effect_room_page.apply_effect_to_video('Black and White', track_index=0, clip_index=3)
        timeline_operation_page.deselect_clip(track_index=0, last_clip_index=3, movement=100)
        playback_window_page.Edit_Timeline_PreviewOperation('Stop')

        main_page.timeline_select_track(track_no=2)  # add a particle effect to track_2
        main_page.enter_room(5)  # Enter Particle room
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Maple')
        tips_area_page.click_TipsArea_btn_insert()

        main_page.enter_room(1)  # Enter Title room, add a title to track_2
        main_page.select_library_icon_view_media('Default')
        tips_area_page.click_TipsArea_btn_insert(option=1)

        main_page.enter_room(4)  # Enter PiP room, add a pip to track_2
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Dialog_03')
        tips_area_page.click_TipsArea_btn_insert(option=1)  # insert

        main_page.enter_room(2)  # Enter Transition room, apply transition to all media
        transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Cross')

        project_new_page.tap_menu_bar_file_pack_project_materials()

        with uuid('d7586be3-4bc4-4a3f-bb35-e3066cba5ac2') as case:
            # 3.3. Current Project Name
            # 3.3.1. Type > New Untitled Project (Default)
            # Pack project w/ name correctly
            default_file_name = project_new_page.find(L.base.file_picker.file_name).AXValue
            check_result = False if not default_file_name == 'Untitled' else True
            case.result = check_result

        with uuid('0f7ea211-2958-453f-ab70-a8eed8d115c0') as case:
            # 3.4. Tags
            # 3.4.1. Type > Empty (Default)
            # Save project w/ tags correctly
            check_result = project_new_page.pack_project.check_default_tags()
            case.result = check_result

        with uuid('8b8e4629-b7a9-4718-8405-70ef1f2acc6e') as case:
            # 3.7. Path
            # 3.7.1. Type > (Default)
            # Save PDR project w/ selected path correctly
            project_new_page.pack_project.unfold_window()
            time.sleep(DELAY_TIME)
            project_new_page.pack_project.set_path(Test_Material_Folder + 'project_operation/')

            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_7_1-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_7_1-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result = project_new_page.compare(ground_truth, current_preview, similarity=0.90)
            case.result = check_result

        with uuid('ad9ad0a8-55c4-4a66-b005-f8f178682724') as case:
            # 3.5. [<] & [>] buttons
            # Enter previous & next folder correctly
            check_result_1 = project_new_page.pack_project.click_previous_folder()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_5_0-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_5_0-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)

            check_result_3 = project_new_page.pack_project.click_next_folder()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_5_0-2.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_5_0-2.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_4 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('ec557d73-9863-4e36-b80a-aff3b04d670a') as case:
            # 3.6. Display Controls
            # 3.6.1. Show Sidebar > On & Off
            # Show & hide sidebar correctly
            check_result_1 = project_new_page.pack_project.click_grouping_show_sidebar(is_enable=False)
            time.sleep(DELAY_TIME)
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_6_1-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_6_1-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)

            check_result_3 = project_new_page.pack_project.click_grouping_show_sidebar(is_enable=True)
            time.sleep(DELAY_TIME)
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_6_1-2.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_6_1-2.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_4 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('da9075f5-9559-42a8-b065-77a21216be69') as case:
            # 3.6. Display Controls
            # 3.6.2. Show items as > Icons
            # Switch item display correctly
            check_result_1 = project_new_page.pack_project.click_grouping_show_item_as_icons()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_6_2-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_6_2-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)

            case.result = check_result_1 and check_result_2

        with uuid('c2ea6579-85d1-43cd-9c88-754839565cbe') as case:
            # 3.6. Display Controls
            # 3.6.2. Show items as > List
            # Show item as settings correctly
            check_result_1 = project_new_page.pack_project.click_grouping_show_item_as_list()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_6_2-2.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_6_2-2.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)

            case.result = check_result_1 and check_result_2

        with uuid('e10b9a48-a5fa-40b4-9cfc-46f75f425660') as case:
            # 3.6. Display Controls
            # 3.6.2. Show items as > Columns
            # Show item as settings correctly
            check_result_1 = project_new_page.pack_project.click_grouping_show_item_as_columns()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_6_2-3.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_6_2-3.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.9)

            case.result = check_result_1 and check_result_2

        with uuid('4db47366-2e0f-4ea9-9347-441167076548') as case:
            # 3. Pack Project
            # 3.1. Library
            # 3.1.1. Media (Photo, Video, Audio)
            # Pack project w/ Content correctly
            check_result_1 = project_new_page.pack_project.click_save()
            time.sleep(DELAY_TIME * 5)

            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == 'New Untitled Project*' else True
            case.result = check_result_1 and check_result_2

        with uuid('e2585605-83ea-45e9-9cc9-b9d930910852') as case:
            # 3.1. Library
            # 3.1.2. Effect
            # Pack project w/ Content correctly
            case.result = check_result_1 and check_result_2

        with uuid('f8b35ad5-0856-42b4-a62a-4eef4f4967d6') as case:
            # 3.1. Library
            # 3.1.3. PiP
            # Pack project w/ Content correctly
            case.result = check_result_1 and check_result_2

        with uuid('8ee08690-9388-4e6d-bfb2-36d268d24962') as case:
            # 3.1. Library
            # 3.1.4. Particle
            # Pack project w/ Content correctly
            case.result = check_result_1 and check_result_2

        with uuid('ed91cb97-10b0-4e10-9952-ce635d935fa4') as case:
            # 3.1. Library
            # 3.1.5. Title
            # Pack project w/ Content correctly
            case.result = check_result_1 and check_result_2

        with uuid('00fda7db-e1a0-45d2-9271-151a4fe0a260') as case:
            # 3.1. Library
            # 3.1.6. Transition
            # Pack project w/ Content correctly
            case.result = check_result_1 and check_result_2

        with uuid('06259a56-76ce-4f05-8109-b311c0bf37fe') as case:
            # 3.2. Aspect Ratio
            # 3.2.1. 4:3
            # Pack project w/ Content correctly
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_2(self):
        main_page.set_project_aspect_ratio('9_16')

        # all video/photo/audio to timeline
        main_page.insert_media('Skateboard 01.mp4', aspect_ratio_conflict_option='no')
        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Food.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Landscape 01.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Speaking Out.mp3')
        tips_area_page.click_TipsArea_btn_insert_audio(option=1)

        main_page.enter_room(3)  # Enter Effect room, add an effect to timeline
        effect_room_page.apply_effect_to_video('Black and White', track_index=0, clip_index=3)
        timeline_operation_page.deselect_clip(track_index=0, last_clip_index=3, movement=100)
        playback_window_page.Edit_Timeline_PreviewOperation('Stop')

        main_page.timeline_select_track(track_no=2)  # add a particle effect to track_2
        main_page.enter_room(5)  # Enter Particle room
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Maple')
        tips_area_page.click_TipsArea_btn_insert()

        main_page.enter_room(1)  # Enter Title room, add a title to track_2
        main_page.select_library_icon_view_media('Default')
        tips_area_page.click_TipsArea_btn_insert(option=1)

        main_page.enter_room(4)  # Enter PiP room, add a pip to track_2
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Dialog_03')
        tips_area_page.click_TipsArea_btn_insert(option=1)  # insert

        main_page.enter_room(2)  # Enter Transition room, apply transition to all media
        transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Cross')

        project_new_page.tap_menu_bar_file_pack_project_materials()

        with uuid('9c6a179a-2844-4be6-ac5b-82dfb5328ad9') as case:
            # 3.3. Current Project Name
            # 3.3.1. Type > Unicode
            # Pack project w/ name correctly
            if not project_new_page.is_exist(L.base.file_picker.main):
                check_result = False
            else:
                check_result = project_new_page.pack_project.set_project_name('9_16_許功蓋_℃ꮤ®¶ÅËæ¾')
            case.result = check_result

        with uuid('c24b8762-c22e-4416-ac7f-ec1e63cc22c0') as case:
            # 3.3. Current Project Name
            # 3.3.1. Type > Big 5 (許功蓋)
            # Pack project w/ name correctly
            case.result = check_result

        with uuid('2ce0a663-87ca-44bc-81ff-8fac2204a202') as case:
            # 3.7. Path
            # 3.7.1. Type > Unicode
            # Save PDR project w/ selected path correctly
            project_new_page.pack_project.unfold_window()
            time.sleep(DELAY_TIME)
            project_new_page.pack_project.set_path(Test_Material_Folder + 'project_operation/路徑許功蓋_℃ꮤ®¶ÅËæ¾/')

            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_7_1-2.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_7_1-2.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result = project_new_page.compare(ground_truth, current_preview, similarity=0.70)
            case.result = check_result

        with uuid('ad187dbe-2dbb-46db-820d-ec0f24383508') as case:
            # 3.7. Path
            # 3.7.1. Type > Big 5 (許功蓋)
            # Save PDR project w/ selected path correctly
            case.result = check_result

        with uuid('09f1a500-e45f-48e0-9e51-ea8d4b729e9a') as case:
            # 3.2. Aspect Ratio
            # 3.2.3. 9:16
            # Pack project w/ Content correctly
            check_result_1 = project_new_page.pack_project.click_save()
            time.sleep(DELAY_TIME * 5)

            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == 'New Untitled Project*' else True
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_3(self):
        main_page.set_project_aspect_ratio('1_1')

        # all video/photo/audio to timeline
        main_page.insert_media('Skateboard 01.mp4', aspect_ratio_conflict_option='no')
        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Food.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Landscape 01.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Speaking Out.mp3')
        tips_area_page.click_TipsArea_btn_insert_audio(option=1)

        main_page.enter_room(3)  # Enter Effect room, add an effect to timeline
        effect_room_page.apply_effect_to_video('Black and White', track_index=0, clip_index=3)
        timeline_operation_page.deselect_clip(track_index=0, last_clip_index=3, movement=100)
        playback_window_page.Edit_Timeline_PreviewOperation('Stop')

        main_page.timeline_select_track(track_no=2)  # add a particle effect to track_2
        main_page.enter_room(5)  # Enter Particle room
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Maple')
        tips_area_page.click_TipsArea_btn_insert()

        main_page.enter_room(1)  # Enter Title room, add a title to track_2
        main_page.select_library_icon_view_media('Default')
        tips_area_page.click_TipsArea_btn_insert(option=1)

        main_page.enter_room(4)  # Enter PiP room, add a pip to track_2
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Dialog_03')
        tips_area_page.click_TipsArea_btn_insert(option=1)  # insert

        main_page.enter_room(2)  # Enter Transition room, apply transition to all media
        transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Cross')

        project_new_page.tap_menu_bar_file_pack_project_materials()

        with uuid('559ee994-ba11-4b01-9a34-898b1a833aad') as case:
            # 3.3. Current Project Name
            # 3.3.1. Type > Symbol
            # Pack project w/ name correctly
            if not project_new_page.is_exist(L.base.file_picker.main):
                check_result = False
            else:
                check_result = project_new_page.pack_project.set_project_name('1_1_@#$%^&* ()_+-{} |[];? <>!')
            case.result = check_result

        with uuid('e1e3107c-2965-4175-8739-76748724ded8') as case:
            # 3.3. Current Project Name
            # 3.3.1. Type > Space Character included
            # Pack project w/ name correctly
            case.result = check_result

        with uuid('b046091f-4dda-4436-8beb-5bc3490d0158') as case:
            # 3.7. Path
            # 3.7.1. Type > Symbol
            # Save PDR project w/ selected path correctly
            project_new_page.pack_project.unfold_window()
            time.sleep(DELAY_TIME)
            project_new_page.pack_project.set_path(Test_Material_Folder + 'project_operation/@#$%^&*()_+{}[]/')

            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_7_1-3.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_7_1-3.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result = project_new_page.compare(ground_truth, current_preview, similarity=0.70)
            case.result = check_result

        with uuid('c576e0fa-62ee-4391-b69c-7c8c5614c97a') as case:
            # 3.2. Aspect Ratio
            # 3.2.4. 1:1
            # Pack project w/ Content correctly
            check_result_1 = project_new_page.pack_project.click_save()
            time.sleep(DELAY_TIME * 5)

            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == 'New Untitled Project*' else True
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_4(self):
        main_page.set_project_aspect_ratio('16_9')

        # all video/photo/audio to timeline
        main_page.insert_media('Skateboard 01.mp4', aspect_ratio_conflict_option='no')
        main_page.select_library_icon_view_media('Skateboard 02.mp4')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Food.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Landscape 01.jpg')
        main_page.tips_area_insert_media_to_selected_track(option=1)
        main_page.select_library_icon_view_media('Speaking Out.mp3')
        tips_area_page.click_TipsArea_btn_insert_audio(option=1)

        main_page.enter_room(3)  # Enter Effect room, add an effect to timeline
        effect_room_page.apply_effect_to_video('Black and White', track_index=0, clip_index=3)
        timeline_operation_page.deselect_clip(track_index=0, last_clip_index=3, movement=100)
        playback_window_page.Edit_Timeline_PreviewOperation('Stop')

        main_page.timeline_select_track(track_no=2)  # add a particle effect to track_2
        main_page.enter_room(5)  # Enter Particle room
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Maple')
        tips_area_page.click_TipsArea_btn_insert()

        main_page.enter_room(1)  # Enter Title room, add a title to track_2
        main_page.select_library_icon_view_media('Default')
        tips_area_page.click_TipsArea_btn_insert(option=1)

        main_page.enter_room(4)  # Enter PiP room, add a pip to track_2
        main_page.select_LibraryRoom_category('General')
        time.sleep(1)
        main_page.select_library_icon_view_media('Dialog_03')
        tips_area_page.click_TipsArea_btn_insert(option=1)  # insert

        main_page.enter_room(2)  # Enter Transition room, apply transition to all media
        transition_room_page.apply_LibraryMenu_Fading_Transition_to_all_video('Cross')

        project_new_page.tap_menu_bar_file_pack_project_materials()

        if not project_new_page.is_exist(L.base.file_picker.main):
            logger('There is not file picker display')
        else:
            project_new_page.pack_project.set_project_name(
                '16_9_12345678901234567890123456789012345678901234567890123456789012345678901234567890'
                + '12345678901234567890123456789012345678901234567890123456789012345678901234567890'
                + '12345678901234567890123456789012345678901234567890123456789012345678901234567890'
                + '123456')

        with uuid('c13aa444-d1b8-4f5c-a691-f815d79b2a52') as case:
            # 3.4. Tags
            # 3.4.1. Type > Work
            # Save project w/ tags correctly
            project_new_page.pack_project.set_tag_to_work()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_4_1-7.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_4_1-7.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result = project_new_page.compare(ground_truth, current_preview, similarity=0.90)
            case.result = check_result

        with uuid('62db2ba5-291f-44d0-b208-5e642c96fd68') as case:
            # 3.4. Tags
            # 3.4.2. Show All
            # show all tag list correctly
            project_new_page.pack_project.click_tags_show_all()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_4_2-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_4_2-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result = project_new_page.compare(ground_truth, current_preview, similarity=0.90)
            case.result = check_result

        with uuid('bda8b3e6-8787-4915-b930-56a2259b5e31') as case:
            # 3.4. Tags
            # 3.4.1. Type > Gray
            # Save project w/ tags correctly
            project_new_page.pack_project.set_tag_to_gray()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_4_1-6.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_4_1-6.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result = project_new_page.compare(ground_truth, current_preview, similarity=0.90)
            case.result = check_result

        with uuid('340d7ce4-8518-4732-a4a2-83f6697136d6') as case:
            # 3.9. Select Folder
            # Save PDR project (*.pdk) correctly as settings
            project_new_page.pack_project.unfold_window()
            time.sleep(DELAY_TIME)
            project_new_page.pack_project.set_path(Test_Material_Folder + 'project_operation/')

            check_result_1 = project_new_page.pack_project.click_save()
            time.sleep(DELAY_TIME * 5)

            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == 'New Untitled Project*' else True
            case.result = check_result_1 and check_result_2

        with uuid('863cc4b0-156a-49b6-b14b-7e0ea44fb4a6') as case:
            # 3.2. Aspect Ratio
            # 3.2.2. 16:9
            # Pack project w/ Content correctly
            case.result = check_result_1 and check_result_2

    # @pytest.mark.skip
    @exception_screenshot
    def test_2_1_5(self):
        main_page.insert_media('Food.jpg')
        project_new_page.tap_menu_bar_file_pack_project_materials()

        with uuid('f7245bf8-ef95-4a8a-be02-66e24609f623') as case:
            # 3.3. Current Project Name
            # 3.3.1. Type > Space Character Only
            # Pack project w/ name correctly
            check_result = project_new_page.pack_project.set_project_name('    ')
            case.result = check_result

        with uuid('01acca45-ef7f-4fb6-aa41-38346eb2e765') as case:
            # 3.8. New Folder
            # 3.8.1. Method > via [New Folder] icon
            # Enter New Folder dialog correctly
            '''
            project_new_page.pack_project.unfold_window()
            time.sleep(DELAY_TIME)
            project_new_page.pack_project.set_path(Test_Material_Folder + 'project_operation/')
            project_new_page.pack_project.click_top_new_folder()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_8_1-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_8_1-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.new_folder.main, file_name=image_full_path)
            check_result = project_new_page.compare(ground_truth, current_preview)
            case.result = check_result

            main_page.press_esc_key()
            '''
            case.result = None
            case.fail_log = 'MacOS limitation'

        with uuid('127767f1-bc5e-4c8f-a235-cc903416808d') as case:
            # 3.8. New Folder
            # 3.8.1. Method > via [New Folder] button
            # Enter New Folder dialog correctly
            project_new_page.save_file.unfold_window()
            time.sleep(DELAY_TIME)
            project_new_page.save_file.set_path(Test_Material_Folder + 'project_operation/')
            time.sleep(DELAY_TIME)
            project_new_page.pack_project.click_bottom_new_folder()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_8_1-2.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_8_1-2.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.new_folder.main, file_name=image_full_path)
            check_result = project_new_page.compare(ground_truth, current_preview, similarity= 0.8)
            case.result = check_result

        with uuid('56e05df7-11ac-4a9a-8d4e-8b3c310970c7') as case:
            # 3.8. New Folder
            # 3.8.2. Type > Untitled folder (Default)
            # Create new folder correctly as settings
            check_result = project_new_page.pack_project.new_folder.check_default_folder_name()
            case.result = check_result

        with uuid('4fcc2831-12c4-44e4-bd0a-4405e6f9145c') as case:
            # 3.8. New Folder
            # 3.8.2. Type > * Empty
            # Grey out [Create] button
            project_new_page.pack_project.new_folder.set_name('')
            time.sleep(DELAY_TIME)

            btn_status = project_new_page.exist(L.base.file_picker.new_folder.btn_create).AXEnabled
            check_result = True if not btn_status else False
            case.result = check_result

        with uuid('e94ac474-1fc9-498a-ab2b-1d9e82a61df5') as case:
            # 3.8. New Folder
            # 3.8.2. Type > Unicode
            # Create new folder correctly as settings
            test_folder_path = Test_Material_Folder + 'project_operation/許功蓋_℃ꮤ®¶ÅËæ¾_@#$%^&*/'
            if os.path.exists(test_folder_path):  # delete last created folder
                import shutil
                shutil.rmtree(test_folder_path)

            check_result = project_new_page.pack_project.new_folder.set_name('許功蓋_℃ꮤ®¶ÅËæ¾_@#$%^&*')
            case.result = check_result

        with uuid('1152c36b-eb29-467e-83c8-7a69ffbe168c') as case:
            # 3.8. New Folder
            # 3.8.2. Type > Big 5 (許功蓋)
            # Create new folder correctly as settings
            case.result = check_result

        with uuid('2396a881-dfc7-44b1-bac7-4f28cc32e9cf') as case:
            # 3.8. New Folder
            # 3.8.2. Type > Symbol
            # Create new folder correctly as settings
            case.result = check_result

        with uuid('fd0d0aaf-561a-4f63-a7b5-7abdd7beeb07') as case:
            # 3.8. New Folder
            # 3.8.4. Cancel > via [Cancel] button
            # Close dialog correctly
            project_new_page.pack_project.new_folder.click_cancel()

            check_result_2 = project_new_page.is_not_exist(L.base.file_picker.new_folder.main)
            case.result = check_result_2

        with uuid('a43ce2ea-68ac-41e2-bfe2-ff70ef003dbd') as case:
            # 3.8. New Folder
            # 3.8.4. Cancel > via [ESC] key
            # Close dialog correctly
            project_new_page.pack_project.click_bottom_new_folder()
            project_new_page.pack_project.new_folder.set_name('許功蓋_℃ꮤ®¶ÅËæ¾_@#$%^&*')
            main_page.press_esc_key()

            check_result = project_new_page.is_not_exist(L.base.file_picker.new_folder.main)
            case.result = check_result

        with uuid('00c6587c-7b5f-45e8-a126-3a660b26f258') as case:
            # 3.8. New Folder
            # 3.8.3. Create > Create
            # Create new folder correctly
            project_new_page.pack_project.click_bottom_new_folder()
            project_new_page.pack_project.new_folder.set_name('許功蓋_℃ꮤ®¶ÅËæ¾_@#$%^&*')
            check_result_1 = project_new_page.pack_project.new_folder.click_create()

            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_3_8_3-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_3_8_3-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.70)
            case.result = check_result_1 and check_result_2

        with uuid('3f4bdb0e-6785-41c1-a979-09bff16f8aa2') as case:
            # 3.10. Cancel
            # 3.10.1. [Cancel] button
            # Close dialog correctly
            project_new_page.pack_project.click_cancel()
            check_result_2 = project_new_page.is_not_exist(L.base.file_picker.main)
            case.result =  check_result_2

        with uuid('c711473f-f6a5-4bb9-a500-7ae98d37ef45') as case:
            # 3.10. Cancel
            # 3.10.2. [ESC] key
            # Close dialog correctly
            project_new_page.tap_menu_bar_file_pack_project_materials()
            time.sleep(DELAY_TIME * 2)
            main_page.press_esc_key()

            check_result = project_new_page.is_not_exist(L.base.file_picker.main)
            case.result = check_result

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_1_1(self):
        with uuid('e790a98e-f400-4139-9b9f-e46f98c12163') as case:
            # 4. Open Project
            # 4.1. Project Type
            # 4.1.1. Timeline is empty
            # Open project correctly as saved content
            check_result_1 = project_new_page.open_pds_project(
                Test_Material_Folder + 'project_operation/project_operation_1.pds')
            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == 'project_operation_1' else True
            case.result = check_result_1 and check_result_2

        with uuid('9b65e2d4-ddad-478b-8d16-459932977903') as case:
            # 4.1. Project Type
            # 4.1.2. Timeline is NON-empty
            # Open project correctly as saved content
            main_page.select_library_icon_view_media('Landscape 01.jpg')
            main_page.tips_area_insert_media_to_selected_track(option=1)
            check_result_1 = project_new_page.open_pds_project(
                Test_Material_Folder + 'project_operation/project_operation_2.pds')
            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == 'project_operation_2' else True
            case.result = check_result_1 and check_result_2

        with uuid('321739db-fe30-4d9f-8cee-718bc9092898') as case:
            # 4.2. Project File
            # 4.2.1. PDS file
            # Open project correctly as saved content
            case.result = check_result_1 and check_result_2

        with uuid('d3b24fb0-dc3b-4cb2-b57c-979b29b0a467') as case:
            # 4.3. Library
            # 4.3.1. Media (Photo, Video, Audio)
            # Open project correctly as saved content
            project_new_page.open_pds_project(Test_Material_Folder + 'project_operation/Untitled.pds')
            current_project_name = main_page.get_project_name()
            check_result_1 = False if not current_project_name == 'Untitled' else True

            # snapshot timeline
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_3_1-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_3_1-1.png'
            current_preview = project_new_page.snapshot(
                locator=main_page.area.timeline, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.8)

            # snapshot aspect ratio btn - 4:3
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_3_1-2.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_3_1-2.png'
            current_preview = project_new_page.snapshot(
                locator=L.main.btn_project_aspect_ratio, file_name=image_full_path)
            check_result_3 = project_new_page.compare(ground_truth, current_preview)

            case.result = check_result_2

        with uuid('c65ee985-d433-436f-8bc4-57bb5ee6382a') as case:
            # 4.8. Path
            # 4.8.1. Type > (Default)
            # Save PDR project w/ selected path correctly
            case.result = check_result_1

        with uuid('cda566b7-7482-46c7-81ca-76a7707dd0e9') as case:
            # 4.5. Name
            # 4.5.1. Type > Untitled (Default)
            # Open project w/ name & Hide unsupported file correctly
            case.result = check_result_1

        with uuid('f635f5f7-7a50-47b9-bcb6-57d97332c623') as case:
            # 4.3. Library
            # 4.3.2. Effect
            # Open project correctly as saved content
            case.result = check_result_2

        with uuid('e78e38a7-a216-46a7-8221-45259001ea8d') as case:
            # 4.3. Library
            # 4.3.3. PiP
            # Open project correctly as saved content
            case.result = check_result_2

        with uuid('8811adeb-f0a6-426a-b20d-d67a2d90242a') as case:
            # 4.3. Library
            # 4.3.4. Particle
            # Open project correctly as saved content
            case.result = check_result_2

        with uuid('54681010-417f-4c42-b1f1-5faeaea272dc') as case:
            # 4.3. Library
            # 4.3.5. Title
            # Open project correctly as saved content
            case.result = check_result_2

        with uuid('caccfe71-6cfb-4e04-a387-29f30a6e5a59') as case:
            # 4.3. Library
            # 4.3.6. Transition
            # Open project correctly as saved content
            case.result = check_result_2

        with uuid('8b63b324-e5b8-4ae4-91f3-b731690ae048') as case:
            # 4.4. Aspect Ratio
            # 4.4.1. 4:3
            # Open project correctly as saved content
            case.result = check_result_3

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_1_2(self):
        with uuid('e4a2a67e-1c5d-4816-9b11-44ca6d58803a') as case:
            # 4.4. Aspect Ratio
            # 4.4.2. 16:9
            # Open project correctly as saved content
            time.sleep(DELAY_TIME*2)
            project_new_page.open_pds_project(
                Test_Material_Folder + 'project_operation/16_9_12345678901234567890123456789012345678901234567890'
                                       '1234567890123456789012345678901234567890123456789012345678901234567890'
                                       '1234567890123456789012345678901234567890123456789012345678901234567890'
                                       '12345678901234567890123456789012345678901234567890123456.pds')

            # snapshot aspect ratio btn - 16:9
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_4_2-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_4_2-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.main.btn_project_aspect_ratio, file_name=image_full_path)
            check_result_1 = project_new_page.compare(ground_truth, current_preview)

            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == '16_9_1234567890123456789012345678901234567890' \
                                                                  '12345678901234567890123456789012345678901234567890' \
                                                                  '12345678901234567890123456789012345678901234567890' \
                                                                  '12345678901234567890123456789012345678901234567890' \
                                                                  '12345678901234567890123456789012345678901234567890' \
                                                                  '123456' else True
            case.result = check_result_1

        with uuid('6de217a9-f11d-42b0-a92c-7a1aa5f71fc5') as case:
            # 4.5. Name
            # 4.5.1. Type > Long
            # Open project w/ name & Hide unsupported file correctly
            case.result = check_result_2

        with uuid('780945f8-f98f-4079-a907-2366697e1e4d') as case:
            # 4.4. Aspect Ratio
            # 4.4.3. 9:16
            # Open project correctly as saved content
            check_result_1 = project_new_page.open_pds_project(
                Test_Material_Folder + 'project_operation/路徑許功蓋_℃ꮤ®¶ÅËæ¾/9_16_許功蓋_℃ꮤ®¶ÅËæ¾.pds')

            # snapshot aspect ratio btn - 9:16
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_4_3-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_4_3-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.main.btn_project_aspect_ratio, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview)

            current_project_name = main_page.get_project_name()
            check_result_3 = False if not current_project_name == '9_16_許功蓋_℃ꮤ®¶ÅËæ¾' else True
            case.result = check_result_2

        with uuid('7836de5f-8686-4cd7-bf2b-618c590756b0') as case:
            # 4.8. Path
            # 4.8.1. Type > Unicode
            # Save PDR project w/ selected path correctly
            case.result = check_result_1

        with uuid('5ea3aa47-8765-48f3-98b6-d42e93729dd5') as case:
            # 4.8. Path
            # 4.8.1. Type > Big 5
            # Save PDR project w/ selected path correctly
            case.result = check_result_1

        with uuid('76121eaa-c16d-4823-98ef-5b101d7d9a13') as case:
            # 4.5. Name
            # 4.5.1. Type > Unicode
            # Open project w/ name & Hide unsupported file correctly
            case.result = check_result_3

        with uuid('bc6df242-f5d6-445a-9c9e-a998d5a25969') as case:
            # 4.5. Name
            # 4.5.1. Type > Big 5
            # Open project w/ name & Hide unsupported file correctly
            case.result = check_result_3

        with uuid('ef83e596-eb23-4fed-9512-f08889032ff9') as case:
            # 4.4. Aspect Ratio
            # 4.4.4. 1:1
            # Open project correctly as saved content
            check_result_1 = project_new_page.open_pds_project(
                Test_Material_Folder + 'project_operation/@#$%^&*()_+{}[]/1_1_@#$%^&* ()_+-{} |[];? <>!.pds')

            current_project_name = main_page.get_project_name()
            check_result_2 = False if not current_project_name == '1_1_@#$%^&* ()_+-{} |[];? <>!' else True

            # snapshot aspect ratio btn - 1:1
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_4_4-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_4_4-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.main.btn_project_aspect_ratio, file_name=image_full_path)
            check_result_3 = project_new_page.compare(ground_truth, current_preview)
            case.result = check_result_3

        with uuid('cda25f86-a8b7-4e98-8d17-605678d76a7d') as case:
            # 4.8. Path
            # 4.8.1. Type > Symbol
            # Save PDR project w/ selected path correctly
            case.result = check_result_1

        with uuid('b9322a2c-0d09-4e25-9cf8-9bdfb52647eb') as case:
            # 4.5. Name
            # 4.5.1. Type > Symbol
            # Open project w/ name & Hide unsupported file correctly
            case.result = check_result_2

        with uuid('a1c307bd-26aa-490e-8a54-8080ca9ae0cf') as case:
            # 4.5. Name
            # 4.5.1. Type > Space Character included
            # Open project w/ name & Hide unsupported file correctly
            case.result = check_result_2

        with uuid('2bd6643c-234c-463b-bd5b-9b842607e693') as case:
            # 4.10. Open
            # 4.10.1. No file missing
            # Open PDR project (*.pds) correctly as settings
            case.result = check_result_2 and check_result_3

    # @pytest.mark.skip
    @exception_screenshot
    def test_3_1_3(self):
        with uuid('e934e31a-bd6d-4a2a-a916-5fad9fa291ac') as case:
            # 4.6. [<] & [>] buttons
            # Enter previous & next folder correctly
            project_new_page.tap_menu_bar_file_open_project()
            time.sleep(DELAY_TIME * 1.5)
            project_new_page.open_project.select_project(
                'project_operation_1.pds', Test_Material_Folder + 'project_operation/')

            check_result_1 = project_new_page.open_project.click_previous_folder()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_6_0-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_6_0-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)

            check_result_3 = project_new_page.open_project.click_next_folder()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_6_0-2.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_6_0-2.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_4 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('401b790f-e80c-4710-acf3-d5ba62a5ec44') as case:
            # 4.7. Display Controls
            # 4.7.1. Show Sidebar > On & Off
            # Show & hide sidebar correctly
            check_result_1 = project_new_page.open_project.click_grouping_show_sidebar(is_enable=False)
            time.sleep(DELAY_TIME)
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_7_1-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_7_1-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)

            check_result_3 = project_new_page.open_project.click_grouping_show_sidebar(is_enable=True)
            time.sleep(DELAY_TIME)
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_7_1-2.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_7_1-2.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_4 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)

            case.result = check_result_1 and check_result_2 and check_result_3 and check_result_4

        with uuid('e2103296-9487-4b95-9822-54ab2eddbf20') as case:
            # 4.7. Display Controls
            # 4.7.2. Show items as > Icons
            # Switch item display correctly
            check_result_1 = project_new_page.open_project.click_grouping_show_item_as_icons()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_7_2-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_7_2-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)

            case.result = check_result_1 and check_result_2

        with uuid('33417a88-3a12-49a9-86da-6e7468833dfa') as case:
            # 4.7. Display Controls
            # 4.7.2. Show items as > List
            # Show item as settings correctly
            check_result_1 = project_new_page.open_project.click_grouping_show_item_as_list()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_7_2-2.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_7_2-2.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)

            case.result = check_result_1 and check_result_2

        with uuid('33d3b5d8-d58c-4728-aadf-d0fc1bebee3c') as case:
            # 4.7. Display Controls
            # 4.7.2. Show items as > Columns
            # Show item as settings correctly
            check_result_1 = project_new_page.open_project.click_grouping_show_item_as_columns()
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_7_2-3.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_7_2-3.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)

            case.result = check_result_1 and check_result_2

        with uuid('c6e160bc-b64e-4586-af17-8ea303b909b8') as case:
            # 4.7. Display Controls
            # 4.7.3. Group items by > Size
            # Show group as settings correctly
            '''
            check_result_1 = project_new_page.open_project.click_grouping_item_by_size()
            time.sleep(2)
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_7_3-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_7_3-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.70)

            case.result = check_result_1 and check_result_2
            '''
            case.result = None
            case.fail_log = 'MacOS limitation'

        with uuid('46e5166b-7dea-49aa-a5a6-41ba5a0dc45b') as case:
            # 4.7. Display Controls
            # 4.7.3. Group items by > Tags
            # Show group as settings correctly
            '''
            check_result_1 = project_new_page.open_project.click_grouping_item_by_tags()
            time.sleep(2)
            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_7_3-2.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_7_3-2.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)

            case.result = check_result_1 and check_result_2

            project_new_page.open_project.click_grouping_menu_item('None')
            '''
            case.result = None
            case.fail_log = 'MacOS limitation'

        with uuid('f14b798c-7cdb-40b0-9134-a3482dab2836') as case:
            # 4.9. New Folder
            # 4.9.1. Method > via [New Folder] icon
            # Enter New Folder dialog correctly
            '''
            project_new_page.open_project.click_top_new_folder()
            time.sleep(DELAY_TIME)

            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_9_1-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_9_1-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.new_folder.main, file_name=image_full_path)
            check_result = project_new_page.compare(ground_truth, current_preview)
            case.result = check_result
            '''
            case.result = None
            case.fail_log = 'MacOS limitation'

        with uuid('c4c1e7d8-8a1b-4c46-a1e4-3afe7d9f5fcb') as case:
            # 4.9. New Folder
            # 4.9.2. Type > Untitled folder (Default)
            # Create new folder correctly as settings
            '''
            check_result = project_new_page.open_project.new_folder.check_default_folder_name()
            case.result = check_result
            '''
            case.result = None
            case.fail_log = 'MacOS limitation'

        with uuid('12001d47-a2fe-48cd-bbc0-a6b31896963a') as case:
            # 4.9. New Folder
            # 4.9.2. Type > * Empty
            # Grey out [Open] button
            '''
            project_new_page.open_project.new_folder.set_name('')
            time.sleep(DELAY_TIME)

            btn_status = project_new_page.exist(L.base.file_picker.new_folder.btn_create).AXEnabled
            check_result = True if not btn_status else False
            case.result = check_result
            '''
            case.result = None
            case.fail_log = 'MacOS limitation'

        with uuid('98c1eaa4-7e04-44ec-af01-a5577539b1bb') as case:
            # 4.9. New Folder
            # 4.9.2. Type > Unicode
            # Create new folder correctly as settings
            '''
            test_folder_path = Test_Material_Folder + 'project_operation/許功蓋_℃ꮤ®¶ÅËæ¾_@#$%^&*/'
            if os.path.exists(test_folder_path):  # delete last created folder
                import shutil
                shutil.rmtree(test_folder_path)

            check_result = project_new_page.open_project.new_folder.set_name('許功蓋_℃ꮤ®¶ÅËæ¾_@#$%^&*')
            case.result = check_result
            '''
            case.result = None
            case.fail_log = 'MacOS limitation'

        with uuid('9a4f97b5-7806-4c94-85de-f314edc992fd') as case:
            # 4.9. New Folder
            # 4.9.2. Type > Big 5
            # Create new folder correctly as settings
            #case.result = check_result
            case.result = None
            case.fail_log = 'MacOS limitation'

        with uuid('50df7c36-db1e-4075-97ea-3d2d3f74ac92') as case:
            # 4.9. New Folder
            # 4.9.2. Type > Symbol
            # Create new folder correctly as settings
            #case.result = check_result
            case.result = None
            case.fail_log = 'MacOS limitation'

        with uuid('177ef79f-9716-434e-bba7-852dd9074d9d') as case:
            # 4.9. New Folder
            # 4.9.4. Cancel > via [Cancel] button
            # Close dialog correctly
            '''
            check_result_1 = project_new_page.open_project.new_folder.click_cancel()

            check_result_2 = project_new_page.is_not_exist(L.base.file_picker.new_folder.main)
            case.result = check_result_1 and check_result_2
            '''
            case.result = None
            case.fail_log = 'MacOS limitation'

        with uuid('931a7a08-0785-4bca-bf5e-b85865c6d9bf') as case:
            # 4.9. New Folder
            # 4.9.4. Cancel > via [ESC] key
            # Close dialog correctly
            '''
            project_new_page.open_project.click_top_new_folder()
            project_new_page.open_project.new_folder.set_name('許功蓋_℃ꮤ®¶ÅËæ¾_@#$%^&*')
            main_page.press_esc_key()

            check_result = project_new_page.is_not_exist(L.base.file_picker.new_folder.main)
            case.result = check_result
            '''
            case.result = None
            case.fail_log = 'MacOS limitation'
        with uuid('a38f99a1-f4cc-42eb-a425-e9231fe0d9b1') as case:
            # 4.9. New Folder
            # 4.9.3. Create > Create
            # Create new folder correctly
            '''
            project_new_page.open_project.click_top_new_folder()
            project_new_page.open_project.new_folder.set_name('許功蓋_℃ꮤ®¶ÅËæ¾_@#$%^&*')
            check_result_1 = project_new_page.open_project.new_folder.click_create()

            image_full_path = Auto_Ground_Truth_Folder + 'project_operation_4_9_3-1.png'
            ground_truth = Ground_Truth_Folder + 'project_operation_4_9_3-1.png'
            current_preview = project_new_page.snapshot(
                locator=L.base.file_picker.main, file_name=image_full_path)
            check_result_2 = project_new_page.compare(ground_truth, current_preview, similarity=0.90)
            case.result = check_result_1 and check_result_2
            '''
            case.result = None
            case.fail_log = 'MacOS limitation'
        with uuid('050872e0-9c39-40ea-a11b-0f6198239d3b') as case:
            # 4.11. Cancel
            # 4.11.1. [Cancel] button
            # Close dialog correctly
            project_new_page.open_project.click_cancel()
            check_result_2 = project_new_page.is_not_exist(L.base.file_picker.main)
            logger(check_result_2)
            case.result = check_result_2

        with uuid('5882577d-3483-47f8-9a07-7d7a72306770') as case:
            # 4.11. Cancel
            # 4.11.2. [ESC] key
            # Close dialog correctly
            project_new_page.tap_menu_bar_file_open_project()
            time.sleep(DELAY_TIME * 2)
            main_page.press_esc_key()

            check_result = project_new_page.is_not_exist(L.base.file_picker.main)
            case.result = check_result

        with uuid('8a1a9e3a-bfb3-4926-83d9-27ae696e0ad3') as case:
            # 4.10. Open
            # 4.10.2. When files are missing
            # Prompt a dialogue to remind user some files are removed or missing
            project_new_page.tap_menu_bar_file_open_project()
            project_new_page.open_project.select_project(
                'FileMissingProject.pds', Test_Material_Folder + 'project_operation/')
            project_new_page.exist_click(L.main.open_file_dialog.btn_open)
            project_new_page.exist_click(L.main.merge_media_to_library_dialog.btn_no)
            time.sleep(DELAY_TIME * 2)
            check_result = project_new_page.open_project.check_file_missing_dialog()
            case.result = check_result

        with uuid('2db4f320-0f82-4caa-bb7c-53da782bfd53') as case:
            # 4.10. Open
            # 4.10.2. When files are missing > [Browse]
            # Prompt a browser to let user to find missing files
            btn_elem = main_page.exist(L.main.cyberlink_powerdirector_dialog.btn_browse)
            project_new_page.open_project.file_missing.click_browse()
            if btn_elem:
                case.result = True
            else:
                case.result = False

        with uuid('0c92847c-c173-42d4-9d4c-ff5852aab7a0') as case:
            # 4.10. Open
            # 4.10.2. When files are missing > [Browse]
            # Open project successfully after finding missing files
            check_result = project_new_page.open_project.file_missing.select_file(
                Test_Material_Folder + '1.jpg')
            case.result = check_result
            time.sleep(DELAY_TIME * 5)

        with uuid('66a2ebde-0286-4344-a368-47a1cb16190c') as case:
            # 4.10. Open
            # 4.10.2. When files are missing > [Ignore]
            # Ignore the missing file after clicking and open project successfully
            logger('2066')
            #project_new_page.tap_menu_bar_file_open_project()
            logger('2068')
            
            #project_new_page.open_project.select_project(
            #    'FileMissingProject.pds', Test_Material_Folder + 'project_operation/')
            #logger('2071')
            #project_new_page.exist_click(L.main.open_file_dialog.btn_open)
            #logger('2073')
            #project_new_page.exist_click(L.main.merge_media_to_library_dialog.btn_no)
            #logger('2075')
            #time.sleep(DELAY_TIME * 2)
           
            btn_elem = main_page.exist(L.main.cyberlink_powerdirector_dialog.btn_ignore)
            project_new_page.open_project.file_missing.click_ignore()
            if btn_elem:
                case.result = True
            else:
                case.result = False


        with uuid('e43b6caf-83ec-4619-9332-b4aa8823501c') as case:
            # 4.10. Open
            # 4.10.2. When files are missing > [Ignore All]
            # Ignore all missing file after clicking and open an empty project correctly
            time.sleep(DELAY_TIME * 2)

            project_new_page.tap_menu_bar_file_open_project()
            project_new_page.open_project.select_project(
                'FileMissingProject.pds', Test_Material_Folder + 'project_operation/')
            project_new_page.exist_click(L.main.open_file_dialog.btn_open)
            project_new_page.exist_click(L.main.merge_media_to_library_dialog.btn_no)
            time.sleep(DELAY_TIME * 2)

            check_ignore_all = main_page.exist(L.main.cyberlink_powerdirector_dialog.btn_ignore_all)

            project_new_page.open_project.file_missing.click_ignore_all()
            time.sleep(DELAY_TIME * 4)
            if check_ignore_all:
                case.result = True
            else:
                case.result = False

    # @pytest.mark.skip
    @exception_screenshot
    def test_skip_case(self):
        with uuid('''
                    9c9abddd-9c77-407b-ba7d-35d5f14e9259
                    7a7ae7ad-cc54-4d17-8e88-68747430ecb5
                    32184edf-f97c-4c74-83f4-95c49e4d4093
                    99724ebf-fb19-4802-8e68-4791b81c1fa2
                    6b71a563-cbea-4e7a-9414-75be27996ad7
                    0de0dbab-3f05-4646-8c25-6ae4821589de
                    98a9e272-4226-4557-9618-90a50610ffc1
                    23ed0d01-f2e8-48c9-8935-071591fb133e
                    2f764673-863a-41bd-9b81-ef2e1841dc69
                    8e415353-0571-418e-ba9f-7db29d3c6737
                    be6b3382-af9b-4933-af08-ec5c25adbdac
                    fdd5d5e5-2e57-45b2-8d91-9feddc81fda3
                    8078779f-ab63-403a-9295-e9165f85a71a
                    25808726-3280-4447-bbd3-16c96f29ef09
                    2d865a97-a361-40cd-8b06-030415b8dd9e
                    ae265eaf-fc8d-4069-a149-7dd3dd67eebf
                    72bfe4e7-acc7-4b6b-9832-150d57fcc010
                    d359ce9d-c430-4c54-803b-109221889b3d
                    de3de32f-eacd-4169-8efe-3a23cf4c6337
                    50fe5f71-4bc3-4f9d-8be4-ba73c972a406
                    2f21e666-6356-4807-8791-3375199fded2
                    0785cbfc-7da5-40fb-a5b5-4ae527e7cd20
                    1a791b09-f511-4740-a0de-b3826097ee19
                    38902e04-5d57-45ab-bb4c-faae80147473
                    d0ce6db7-b6b0-4b70-a239-745731d71cfb
                    dc9cc61f-d797-4d07-9f7e-c7bd077b14f1
                    77b1de40-a335-49bb-b804-b190f5c1d264
                    c679a303-fed5-497b-b596-b03f2416ff45
                    b6ee057b-868d-4ee7-a0c9-637177106b85
                    f217ca14-8477-4ae6-bf91-639c2b3eaf5b
                    7f074722-61cf-486f-9383-251631cb6bb5
                    e2aadb89-4346-4afa-84af-7c3f13d28400
                    4885bb99-0f71-4934-b7fa-df5db15c3cf6
                    a8f3f4f0-7249-4215-b842-ca2873e3be4a
                    e82d5356-6d70-4b04-b9f0-eee736e50450
                    eb7eda2b-60f9-46f5-b572-3f5fa3c12da1
                    bbe6ed54-26cd-4b4c-a187-d5209d19e131
                    2dea98da-4a90-42bc-b8d8-e24ceaefae77
                    900f10c2-c2f2-4e20-aaa3-b11d629eb085
                    54ed62b7-972e-46eb-a668-c23ebf03a1cc
                    0f179fe1-90ea-4810-a33e-ef00b4b4633a
                    03bc41c4-8f59-4d1e-88e2-df76ad1320ea
                    55169e17-de2e-4449-b9b8-b3956177cad1
                    36394001-6579-4f1d-b25a-8ef553458693
                    b2690351-de0e-4722-ae6e-25ae34dbbc97
                    3606a340-add2-44e9-8482-f63081f78345
                    a07fe602-a45c-4969-8362-2b5cbb891a0a
                    63dc3c26-3739-468e-bde8-de217e612a10
                    05982064-1aed-498e-ade1-d50552df1994
                    104a595b-5b51-48a8-a9ad-3ab4fcac48d5
                    5d15a3d6-6b9c-4e48-8e73-5ffff8e538cd
                    a32905ce-d788-4632-92db-93f0fec588e1
                    4091e5f4-217d-47a0-ae79-1b6a69036cab
                    9d750504-95b7-4802-856a-4533d8de028c
                    9ddb81c9-ee44-42b9-8006-2f41977ba1e2
                    5b3e9d79-ccf3-4910-8d2c-0f543d899ef3
                    ecc7e0e4-5270-4be2-be61-9293c2f768d3
                    f12ec407-b5a1-457b-9f59-dfd28d9b18e9
                    43b052ca-262e-49ba-8ae4-fbeb8b0dad1e
                    0e2347d8-06d4-4e97-bf07-ad4c06a44ffc
                    b5dbe776-7edc-430b-b9de-1c1a1eb63f5b
                    28629f8d-996b-4496-bbce-e52dde19debb
                    cf6cce9f-e887-4034-90b2-8ed0079e1b80
                    36d591a6-3b79-47de-b792-8f49866f18db
                    4ccfa413-b7f2-4813-9a25-5dbe9d517f65
                    12001d47-a2fe-48cd-bbc0-a6b31896963a
                    2bd6643c-234c-463b-bd5b-9b842607e693
                    ''') as case:
            case.result = None
            case.fail_log = '*SKIP by AT*'



